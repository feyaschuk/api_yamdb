from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    DEFAULT_USER = 'user'
    USER_STATUSES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    ]
    user_status = models.CharField(
        choices=USER_STATUSES,
        default=DEFAULT_USER
    )
    email = models.EmailField(
        max_length=150,
        unique=True
    )


class Category(models.Model):
    title = models.CharField(max_length=200,
                             help_text='Укажите название категории')
    slug = models.SlugField(max_length=150, unique=True,
                            verbose_name='Идентификатор категории',)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Категория'

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(max_length=200,
                             help_text='Укажите жанр')
    slug = models.SlugField(max_length=150, unique=True,
                            verbose_name='Идентификатор жанра',)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Жанр'

    def __str__(self):
        return self.title


class Title(models.Model):
    title = models.CharField(max_length=200,)
    year = models.IntegerField(verbose_name="Год выпуска")
    rating = models.FloatField()
    description = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='title',
                                 verbose_name='Категория')
    genre = models.ManyToManyField(Genre, verbose_name='Жанр', blank=True)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Название'

    def __str__(self):
        return self.title[:15]
