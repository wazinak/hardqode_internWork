from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Доступен',
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_course_title'
            )
        ]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        blank=True,
        null=True,
    )
    constraints = [
        models.UniqueConstraint(
            fields=['course', 'title'],
            name='unique_course_title_lesson'
        )
    ]

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    students = models.ManyToManyField(
        User,
        verbose_name='Студенты в группе',
        related_name='in_groups',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'title'],
                name='unique_course_title'
            )
        ]
