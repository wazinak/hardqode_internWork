from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import Course
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Владелец кошелька',
        related_name='balance'
    )
    balance = models.DecimalField(
        verbose_name='Баланс',
        max_digits=10,
        decimal_places=2,
        default=1000,
    )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    def save(self, *args, **kwargs):
        if self.balance < 0:
            raise ValidationError("Баланс не может быть меньше 0.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Баланс {self.user.get_full_name()} = {self.balance}'


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Пользователь')
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
    )
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Начало подписки'
    )
    end_date = models.DateTimeField(
        verbose_name='Дата окончания подписки'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)


    def __str__(self):
        return f'Подписка {self.user} на {self.course}'
