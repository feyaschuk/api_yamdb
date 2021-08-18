from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserRoles():
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLE_CHOICES = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]


class User(AbstractUser):
    role = models.CharField(
        max_length=150,
        choices=UserRoles.USER_ROLE_CHOICES,
        default=UserRoles.USER,
        verbose_name='user_role'
    )
    bio = models.TextField(blank=True, null=True, verbose_name='user_bio')
    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name='user_email'
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
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles_category',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(Genre, verbose_name='Жанр', blank=True)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Название'

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    text = models.CharField(max_length=200)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=(MinValueValidator(1),
                    MaxValueValidator(10))
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews_title')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('title', 'author',)


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата комментария', auto_now_add=True, db_index=True)
