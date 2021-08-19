import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserRoles:
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
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
        verbose_name="Роль пользователя",
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Биография пользователя",
    )
    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name="E-Mail пользователя",
    )

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Укажите название категории",
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name="Идентификатор категории",
    )

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Категория"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Укажите жанр",
        verbose_name="Название жанра",
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Идентификатор жанра",
    )

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Жанр"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название произведения",
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска",
        validators=[
            MaxValueValidator(
                dt.datetime.now().year,
                "Год не может быть больше текущего",
            )
        ],
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Описание произведения",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="titles",
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        blank=True,
    )

    class Meta:
        ordering = ("id",)
        verbose_name_plural = "Название"

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    text = models.CharField(
        max_length=200,
        verbose_name="Текст отзыва",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    score = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        verbose_name="Оценка",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews_title",
        verbose_name="Произведение",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата отзыва",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique_together_title_author",
            )
        ]
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата комментария",
    )

    class Meta:
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:15]
