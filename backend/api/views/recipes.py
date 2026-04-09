from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import RecipePagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers.recipe_mini import RecipeMiniSerializer
from api.serializers.recipes import (IngredientSerializer,
                                     RecipeReadSerializer,
                                     RecipeWriteSerializer, TagSerializer)
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = RecipePagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_queryset(self):
        return Recipe.objects.with_user_annotations(self.request.user)

    def _add_to_model(self, request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        obj, created = model.objects.get_or_create(user=user, recipe=recipe)
        if not created:
            return Response(
                {'detail': f'Рецепт уже в {model._meta.verbose_name}.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = RecipeMiniSerializer(
            recipe,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _remove_from_model(self, request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        deleted, _ = model.objects.filter(
            user=user,
            recipe=recipe,
        ).delete()
        if deleted == 0:
            return Response(
                {'detail': f'Рецепта нет в {model._meta.verbose_name}.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['get'],
        url_path='get-link',
    )
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        short_url = request.build_absolute_uri(
            reverse(
                'redirect_short_link',
                kwargs={'short_code': recipe.short_code},
            )
        )
        return Response(
            {'short-link': short_url},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        return self._add_to_model(request, pk, ShoppingCart)

    @shopping_cart.mapping.delete
    def remove_from_cart(self, request, pk=None):
        return self._remove_from_model(request, pk, ShoppingCart)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__shoppingcart_set__user=user)
            .values(
                'ingredient__name',
                'ingredient__measurement_unit',
            )
            .annotate(total_amount=Sum('amount'))
            .order_by('ingredient__name')
        )
        lines = [
            f"{item['ingredient__name']} "
            f"({item['ingredient__measurement_unit']}) — "
            f"{item['total_amount']}"
            for item in ingredients
        ]
        content = '\n'.join(lines)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        return self._add_to_model(request, pk, Favorite)

    @favorite.mapping.delete
    def remove_from_favorite(self, request, pk=None):
        return self._remove_from_model(request, pk, Favorite)
