from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .message_creators import send_confirmation_code
from .permissions import (CustomIsAuthenticated, IsAdminOrReadOnly,
                          IsAdminOrSuperUser, IsModeratorOrAdminOrReadOnly,
                          IsOwnerOrModeratorOrAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserSerializer, GenreSerializer,
                          ReviewSerializer, SignUpSerializer, TitleSerializer,
                          UserMeSerializer)


class MixinsViewSet(mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsModeratorOrAdminOrReadOnly,
        IsOwnerOrModeratorOrAdminOrReadOnly,
    ]
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("titles_id"))        
        return serializer.save(author=self.request.user, title_id=title.id)

    def get_queryset(self):
        title_id = self.kwargs.get('titles_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews_title.all()


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsModeratorOrAdminOrReadOnly,
        IsOwnerOrModeratorOrAdminOrReadOnly,
    ]
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class CategoryViewSet(MixinsViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly, ]
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class GenreViewSet(MixinsViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly, ]
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
        return Response(
            {'error_message': 'Not all required fields are filled in!'},
            status=status.HTTP_400_BAD_REQUEST
        )
    current_user = get_object_or_404(User, username=username)
    if current_user.password != confirmation_code:
        return Response(
            {'error_message': 'Confirmation code is not correct!'},
            status=status.HTTP_400_BAD_REQUEST
        )
    token = AccessToken.for_user(current_user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    search_fields = ('username',)
    permission_classes = [CustomIsAuthenticated, IsAdminOrSuperUser, ]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,),
        serializer_class=UserMeSerializer
    )
    def me(self, request):
        user_me = User.objects.get(username=self.request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user_me)
            response = Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user_me,
                data=request.data,
                partial=True
            )
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_200_OK)
        return response
