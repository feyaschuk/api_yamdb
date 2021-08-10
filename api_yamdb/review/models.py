from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
class Title(models.Model):
    pass

class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.OneToOneField(
        Title, on_delete=models.CASCADE, related_name='reviews')
    #score = models.ForeignKey(
        #Title, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, blank=True, null=True, related_name='reviews_title')
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