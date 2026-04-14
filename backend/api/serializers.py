import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Subscription, User


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для декодирования base64 изображений."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)
        return super().to_internal_value(data)


class ApiUserSerializer(UserSerializer):
    """Сериализатор пользователя."""

    is_subscribed = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return bool(
            request
            and request.user.is_authenticated
            and Subscription.objects.filter(
                user=request.user,
                author=obj
            ).exists()
        )

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else None


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для аватара."""

    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)

    def to_representation(self, instance):
        return {'avatar': instance.avatar.url if instance.avatar else None}


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в рецепте."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Короткий сериализатор для рецептов."""

    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def get_image(self, obj):
        return obj.image.url if obj.image else None


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения рецептов."""

    author = ApiUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(
        many=True,
        source='ingredient_in_recipe'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = (
            'pub_date',
            'short_code',
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return bool(
            request
            and request.user.is_authenticated
            and Favorite.objects.filter(
                user=request.user,
                recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return bool(
            request
            and request.user.is_authenticated
            and ShoppingCart.objects.filter(
                user=request.user,
                recipe=obj
            ).exists()
        )

    def get_image(self, obj):
        return obj.image.url if obj.image else None


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления рецептов."""

    ingredients = IngredientWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Recipe
        exclude = (
            'pub_date',
            'short_code',
        )

    def _create_ingredients(self, recipe, ingredients):
        IngredientInRecipe.objects.bulk_create([
            IngredientInRecipe(
                recipe=recipe,
                ingredient=item['ingredient'],
                amount=item['amount']
            )
            for item in ingredients
        ])

    def validate(self, data):
        ingredients = data.get('ingredients')
        tags = data.get('tags', [])

        if not ingredients:
            raise serializers.ValidationError('Нужен хотя бы один ингредиент')

        ingredient_ids = [item['ingredient'].id for item in ingredients]

        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться'
            )

        if not tags:
            raise serializers.ValidationError('Нужен хотя бы один тег')

        if len(tags) != len(set(tags)):
            raise serializers.ValidationError('Теги не должны повторяться')

        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        self._create_ingredients(recipe, ingredients)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        instance = super().update(instance, validated_data)

        instance.tags.set(tags)

        instance.ingredient_in_recipe.all().delete()
        self._create_ingredients(instance, ingredients)

        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data


class SubscriptionSerializer(ApiUserSerializer):
    """Сериализатор для подписок с рецептами."""

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count',
            'is_subscribed',
            'avatar'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            try:
                limit = int(recipes_limit)
                if limit > 0:
                    recipes = recipes[:limit]
            except (ValueError, TypeError):
                pass
        return ShortRecipeSerializer(
            recipes, many=True, context=self.context
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания подписки."""

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Subscription
        fields = ('user', 'author')

    def validate(self, data):
        user = data['user']
        author = data['author']

        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя'
            )

        if Subscription.objects.filter(
            user=user,
            author=author
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны'
            )

        return data

    def create(self, validated_data):
        return Subscription.objects.create(**validated_data)


class UserRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для избранного и корзины."""

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('user', 'recipe')
        abstract = True

    def validate(self, data):
        user = data['user']
        recipe = data['recipe']
        model = self.Meta.model

        if model.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен'
            )

        return data

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe,
            context=self.context
        ).data


class FavoriteSerializer(UserRecipeSerializer):
    class Meta(UserRecipeSerializer.Meta):
        model = Favorite


class ShoppingCartSerializer(UserRecipeSerializer):
    class Meta(UserRecipeSerializer.Meta):
        model = ShoppingCart
