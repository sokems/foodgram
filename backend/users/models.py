from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    """
    Модель пользователя.
    Использует email как основной идентификатор.
    """

    email = models.EmailField(
        'Email',
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.MAX_NAME_LENGTH
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.MAX_NAME_LENGTH
    )

    avatar = models.ImageField(
        'Аватар',
        upload_to='users/',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('last_name', 'first_name', 'username')
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """
    Модель подписки пользователей.
    Пользователь (user) подписывается на автора (author)
    """

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
                fields=('user', 'author'),
                name='unique_subscription'
            ),
            models.CheckConstraint(
                condition=~models.Q(user=models.F('author')),
                name='prevent_self_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user} → {self.author}'
