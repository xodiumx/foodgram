from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Модель для пользователей.
    Attributes:
        username: отображаемое имя пользователя.
        email: почта пользователя.
        first_name: имя.
        last_name: фамилия.
    """
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        null=False,
        blank=False
    )

    class Meta:
        ordering = ('id',)
        verbose_name = ('Пользователь')
        verbose_name_plural = ('Пользователи')

    def __str__(self):
        return self.username


class Follow(models.Model):
    """
    Модель для подписок.
    Attributes:
        user: текущий user.
        following: на кого подписываются.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('following', 'user'),
                name='unique_user_following',
                violation_error_message='Повторная подписка',
            )
        ]
        verbose_name = ('Подписка')
        verbose_name_plural = ('Подписки')
