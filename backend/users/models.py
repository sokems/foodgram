from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram.constants import (EMAIL_MAX_LENGTH, NAME_MAX_LENGTH,
                                USERNAME_MAX_LENGTH, USERNAME_REGEX)


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[USERNAME_REGEX],
        verbose_name='Имя пользователя',
    )
    first_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Фамилия',
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['email']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписки пользователя на автора."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_subscription',
            ),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
