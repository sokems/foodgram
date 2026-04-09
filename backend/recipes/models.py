import shortuuid
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Exists, Manager, OuterRef

from foodgram.constants import (COOKING_TIME_MAX, COOKING_TIME_MIN,
                                INGREDIENT_MAX_AMOUNT,
                                INGREDIENT_MEASURE_MAX_LENGTH,
                                INGREDIENT_MIN_AMOUNT,
                                INGREDIENT_NAME_MAX_LENGTH,
                                RECIPE_NAME_MAX_LENGTH, TAG_NAME_MAX_LENGTH,
                                UUID_MAX_LENGTH)

User = get_user_model()


class RecipeManager(Manager):
    """Менеджер для модели рецептов."""

    def with_user_annotations(self, user):
        if not user.is_authenticated:
            return self.get_queryset().annotate(
                is_favorited=Exists(Favorite.objects.none()),
                is_in_shopping_cart=Exists(ShoppingCart.objects.none()),
            )

        favorite_subquery = Favorite.objects.filter(
            user=user,
            recipe=OuterRef('pk'),
        )
        cart_subquery = ShoppingCart.objects.filter(
            user=user,
            recipe=OuterRef('pk'),
        )
        return self.get_queryset().annotate(
            is_favorited=Exists(favorite_subquery),
            is_in_shopping_cart=Exists(cart_subquery),
        )


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        max_length=TAG_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Название тега',
    )
    slug = models.SlugField(
        max_length=TAG_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        max_length=INGREDIENT_NAME_MAX_LENGTH,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=INGREDIENT_MEASURE_MAX_LENGTH,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
            ),
        ]

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    """Модель рецепта."""

    objects = RecipeManager()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=RECIPE_NAME_MAX_LENGTH,
        verbose_name='Название рецепта',
    )
    text = models.TextField(verbose_name='Описание рецепта')
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Картинка',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (мин)',
        validators=[
            MinValueValidator(
                COOKING_TIME_MIN,
                message=(
                    f'Время приготовления не может быть меньше '
                    f'{COOKING_TIME_MIN} минут.'
                ),
            ),
            MaxValueValidator(
                COOKING_TIME_MAX,
                message=(
                    f'Время приготовления не может быть больше '
                    f'{COOKING_TIME_MAX} минут.'
                ),
            ),
        ],
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    recipe_ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='used_in_recipes',
        verbose_name='Ингредиенты',
    )
    short_code = models.CharField(
        max_length=UUID_MAX_LENGTH,
        unique=True,
        default=shortuuid.uuid,
        verbose_name='Короткий код',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель ингредиента в рецепте."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                INGREDIENT_MIN_AMOUNT,
                message=(
                    f'Количество ингредиента не может быть меньше '
                    f'{INGREDIENT_MIN_AMOUNT}.'
                ),
            ),
            MaxValueValidator(
                INGREDIENT_MAX_AMOUNT,
                message=(
                    f'Количество ингредиента не может быть больше '
                    f'{INGREDIENT_MAX_AMOUNT}.'
                ),
            ),
        ],
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient',
            ),
        ]

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class UserRecipeRelation(models.Model):
    """Абстрактная базовая модель для связи пользователя и рецепта."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_%(class)s',
            )
        ]


class Favorite(UserRecipeRelation):
    """Модель избранного рецепта."""

    class Meta(UserRecipeRelation.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user} ♥ {self.recipe}'


class ShoppingCart(UserRecipeRelation):
    """Модель списка покупок."""

    class Meta(UserRecipeRelation.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user} → {self.recipe}'
