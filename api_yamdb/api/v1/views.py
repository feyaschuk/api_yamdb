from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from reviews.models import Comment, Review, User, Title
from .serializers import (CommentSerializer, ReviewSerializer,
                          CustomUserSerializer, SignUpSerializer)
from .message_creators import send_confirmation_code


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
    serializer_class = CustomUserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def create_new_user(request):
    serializer = SignUpSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = request.data['username']
    email = request.data['email']
    confirmation_code = User.objects.make_random_password()
    send_confirmation_code(username, email, confirmation_code)
    serializer.save(password=confirmation_code)
    return Response(serializer.data, status=status.HTTP_200_OK)
