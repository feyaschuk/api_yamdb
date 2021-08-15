from django.contrib.auth import get_user_model
from django.db.models.aggregates import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from rest_framework.fields import CurrentUserDefault
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True) 
    
    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('author', 'title')


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        fields = '__all__'
        model = Comment    
        read_only_fields = ('author', 'review')

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User

    def validate(self, data):
        if data['username'] == 'me':
            raise validators.ValidationError(
                'You can not use this username.'
            )
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
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
    rating = serializers.SerializerMethodField()
        
    category = RepresentCategory(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = RepresentGenre(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=False
    )
    
    def get_rating(self, obj):        
        rating = Review.objects.filter(title=obj.id).aggregate(Avg('score'))
        if rating['score__avg'] is None:
            return None
        return rating['score__avg']     
       

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
