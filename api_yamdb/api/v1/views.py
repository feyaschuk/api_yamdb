from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Avg
from rest_framework import viewsets, status, filters, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, permissions, serializers
from rest_framework.pagination import PageNumberPagination

from reviews.models import (Comment, Review, User, Title,
                            Category, Genre)
from .serializers import (CommentSerializer, ReviewSerializer, CategorySerializer,
                          CustomUserSerializer, SignUpSerializer, TitleSerializer,
                          GenreSerializer)
from .message_creators import send_confirmation_code
from .permissions import *
# from .filters import TitleFilter



class MixinsViewSet(mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    pass



class ReviewViewSet(viewsets.ModelViewSet):       
    #permission_classes = [IsModeratorOrAdminOrReadOnly,IsOwnerOrReadOnly]   
    serializer_class = ReviewSerializer    
    pagination_class = PageNumberPagination
    
    def perform_create(self, serializer):        
        title = get_object_or_404(Title, pk=self.kwargs.get("titles_id"))
        if Review.objects.filter(author=self.request.user, title_id=title.id).exists():
            raise serializers.ValidationError("You can send only one review for one title.")   
        return serializer.save(author=self.request.user, title_id=title.id) 

    def get_queryset(self):
        title_id = self.kwargs.get("titles_id")
        title = get_object_or_404(Title, id=title_id)
        return Review.objects.filter(title=title)
    

class CommentViewSet(viewsets.ModelViewSet): 
    permission_classes = [IsModeratorOrAdminOrReadOnly, ] 
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))              
        return serializer.save(author=self.request.user, review=review) 

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    #filterset_class = TitleFilter
    
    
class CategoryViewSet(MixinsViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'
    

class GenreViewSet(MixinsViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


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


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    search_fields = ('username',)
    permission_classes = [CustomIsAuthenticated, IsAdminOrSuperUser, ]

