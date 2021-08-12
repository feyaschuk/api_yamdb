from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from reviews.models import Comment, Review, User
from reviews.models import Title
from django.db.models import Avg
from django.http import JsonResponse 

from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination

from .permissions import IsOwnerOrReadOnly, IsAdminOnly, IsModeratorOrReadOnly
from .serializers import (CommentSerializer, ReviewSerializer,UserSerializer, TitleSerializer)

class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]    
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination
    
    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("titles_id"))
        serializer.save(title=title)
        #serializer.save(author=self.request.user, title=title) добавить автора, когда User будет готов

    def get_queryset(self):
        title_id = self.kwargs.get("titles_id")
        title = get_object_or_404(Title, pk=title_id)
        return Review.objects.filter(title=title)
    
class CommentViewSet(viewsets.ModelViewSet): 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]    
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(review=review)
        #serializer.save(author=self.request.user, review=review) добавить автора, когда User будет готов

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOnly,]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'retrieve':
            return (IsAdminOnly(),)
        return super().get_permissions()

#@permission_required(IsAdminOnly)
class TitleViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAdminUser]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
