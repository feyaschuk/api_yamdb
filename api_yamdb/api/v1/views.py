from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Avg
from django.http import JsonResponse 

from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination

from reviews.models import Comment, Review, User, Title
from .serializers import (CommentSerializer, ReviewSerializer,
                          CustomUserSerializer, SignUpSerializer, TitleSerializer)
from .message_creators import send_confirmation_code


from .permissions import IsOwnerOrReadOnly, IsAdminOnly, IsModeratorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]    
    serializer_class = ReviewSerializer    
    pagination_class = PageNumberPagination
    
    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("titles_id"))        
        return serializer.save(author=self.request.user, title=title) #добавить автора, когда User будет готов

    def get_queryset(self):
        title_id = self.kwargs.get("titles_id")
        title = get_object_or_404(Title, id=title_id)
        return Review.objects.filter(title=title)

class CommentViewSet(viewsets.ModelViewSet): 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]      
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        #return serializer.save(review=review)
        return serializer.save(author=self.request.user, review=review) #добавить автора, когда User будет готов

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()


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


@api_view(['POST'])
@permission_classes([AllowAny])
def create_access_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    if username is None or confirmation_code is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    current_user = get_object_or_404(User, username=username)
    if current_user.password != confirmation_code:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(current_user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)

class TitleViewSet(viewsets.ModelViewSet): 
    queryset = Title.objects.all()  
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
