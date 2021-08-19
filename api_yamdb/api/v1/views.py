from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (CustomIsAuthenticated, IsAdmin, IsModerator, IsOwner,
                          IsSafeMethod, IsSuperUser)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserSerializer, GenreSerializer,
                          ReviewSerializer, SignUpSerializer, TitleSerializer,
                          TokenCreateSerializer, UserMeSerializer)


class DestroyListCreateViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [
        CustomIsAuthenticated
        & (IsOwner | IsModerator | IsAdmin | IsSuperUser)
        | IsSafeMethod,
    ]
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("titles_id"))
        return serializer.save(author=self.request.user, title_id=title.id)

    def get_queryset(self):
        title_id = self.kwargs.get("titles_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews_title.all()


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [
        CustomIsAuthenticated
        & (IsOwner | IsModerator | IsAdmin | IsSuperUser)
        | IsSafeMethod,
    ]
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review = title.reviews_title.get(id=self.kwargs.get("review_id"))
        return review.comments.all()


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [
        CustomIsAuthenticated & (IsAdmin | IsSuperUser) | IsSafeMethod
    ]
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class CategoryViewSet(DestroyListCreateViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [
        CustomIsAuthenticated & (IsAdmin | IsSuperUser) | IsSafeMethod
    ]
    search_fields = ("name", "slug")
    lookup_field = "slug"


class GenreViewSet(DestroyListCreateViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [
        CustomIsAuthenticated & (IsAdmin | IsSuperUser) | IsSafeMethod
    ]
    search_fields = ("name", "slug")
    lookup_field = "slug"


@api_view(["POST"])
@permission_classes([AllowAny])
def create_new_user(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data["username"]
    email = request.data["email"]
    confirmation_code = User.objects.make_random_password()
    send_mail(
        "Confirmation code from YamDb",
        f"Dear {username}, you confirmation code: {confirmation_code}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    serializer.save(password=confirmation_code)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def create_access_token(request):
    serializer = TokenCreateSerializer(data=request.data)
    username = request.data.get("username")
    serializer.is_valid(raise_exception=True)
    current_user = get_object_or_404(User, username=username)
    token = AccessToken.for_user(current_user)
    return Response({"token": str(token)}, status=status.HTTP_200_OK)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = "username"
    search_fields = ("username",)
    permission_classes = [CustomIsAuthenticated & (IsAdmin | IsSuperUser)]

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=(IsAuthenticated,),
        serializer_class=UserMeSerializer,
    )
    def me(self, request):
        user_me = User.objects.get(username=self.request.user.username)
        if request.method == "GET":
            serializer = self.get_serializer(user_me)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            user_me, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
