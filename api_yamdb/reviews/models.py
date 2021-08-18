import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    DEFAULT_USER = 'user'
    USER_STATUSES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    ]
    role = models.CharField(
        max_length=150,
        choices=USER_STATUSES,
        default=DEFAULT_USER
    )
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(
        max_length=150,
        unique=True
    )


class Category(models.Model):
    name = models.CharField(max_length=200,
                            help_text='Укажите название категории')
    slug = models.SlugField(max_length=150, unique=True,
                            verbose_name='Идентификатор категории',)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Укажите жанр')
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True,
                            verbose_name='Идентификатор жанра',)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200,)
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска')
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска',
                                            validators=[
                                                        MaxValueValidator(dt.datetime.now().year,
                                                              'Год не может быть больше текущего')
                                                       ]
                                            )
    description = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(Genre, verbose_name='Жанр', blank=True)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Название'

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    text = models.CharField(max_length=200, verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор отзыва')
    score = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),
                    MaxValueValidator(10)),
        verbose_name='Оценка'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews_title',
        verbose_name='Произведение')
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата отзыва')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_togather_title_author')]
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв')
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата комментария')

    class Meta:
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
