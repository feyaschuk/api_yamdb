from django.shortcuts import get_object_or_404
from reviews.models import Comment, Review, User
from reviews.models import Title
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (CommentSerializer, ReviewSerializer,UserSerializer)

class ReviewViewSet(viewsets.ModelViewSet):    
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    
    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("titles_id"))
        serializer.save(title=title)

    def get_queryset(self):
        title_id = self.kwargs.get("titles_id")
        title = get_object_or_404(Title, pk=title_id)
        return Review.objects.filter(title=title)
    
class CommentViewSet(viewsets.ModelViewSet):    
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
