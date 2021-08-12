from reviews.models import Comment, Review, User
from reviews.models import Title, Category, Genre
from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Comment    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'slug')
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class RepresentCategory(serializers.SlugRelatedField):
    def to_representation(self, obj):
        serializer = CategorySerializer(obj)
        return serializer.data


class RepresentGenre(serializers.SlugRelatedField):
    def to_representation(self, obj):
        serializer = GenreSerializer(obj)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = RepresentCategory(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = RepresentGenre(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
