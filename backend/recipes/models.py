import random
import string

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.conf import settings
from users.models import User


class Tag(models.Model):
    """Модель тегов"""

    name = models.CharField(
        'Название',
        max_length=settings.MAX_TAG_NAME_LENGTH,
        unique=True
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=settings.MAX_TAG_SLUG_LENGTH,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов"""

    name = models.CharField(
        'Название',
        max_length=settings.MAX_INGREDIENT_NAME_LENGTH
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=settings.MAX_MEASUREMENT_UNIT_LENGTH
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель рецептов"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        'Название',
        max_length=settings.MAX_RECIPE_NAME_LENGTH
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/'
    )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (мин)',
        validators=(
            MinValueValidator(settings.MIN_COOKING_TIME),
            MaxValueValidator(settings.MAX_COOKING_TIME)
        )
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    short_code = models.CharField(
        max_length=settings.MAX_SHORT_CODE_NAME_LENGTH,
        unique=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.name} ({self.author})'

    def save(self, *args, **kwargs):
        if not self.short_code:
            while True:
                code = ''.join(
                    random.choices(string.ascii_letters + string.digits, k=6)
                )
                if not Recipe.objects.filter(short_code=code).exists():
                    self.short_code = code
                    break
        super().save(*args, **kwargs)


class IngredientInRecipe(models.Model):
    """Промежуточная модель ингредиентов"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(settings.MIN_INGREDIENT_AMOUNT),
            MaxValueValidator(settings.MAX_INGREDIENT_AMOUNT)
        )
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'
            ),
        )

    def __str__(self):
        return (f'{self.ingredient.name} '
                f'- {self.amount} {self.ingredient.measurement_unit}')


class Favorite(models.Model):
    """Модель избранного"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            ),
        )

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name}'


class ShoppingCart(models.Model):
    """Модель списка покупок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            ),
        )

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name}'
