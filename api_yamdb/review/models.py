from django.db import models
from django.contrib.auth.models import AbstractUser

CHOICES=[]

class User(AbstractUser):
    pass

class Category(models.Model):
    pass

class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateTimeField()
    rating = models.FloatField()
    description = models.TextField()
    genre = models.CharField(max_length=200)
    group = (models.ForeignKey(Category, on_delete=models.SET_NULL,
             blank=True, null=True, related_name="titles"))

class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.OneToOneField(
        Title, on_delete=models.CASCADE, related_name='reviews')
    #score = models.ForeignKey(
        #Title, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата комментария', auto_now_add=True, db_index=True)