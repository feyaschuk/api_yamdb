
from django.db.models.aggregates import Avg
from reviews.models import Comment, Review, Title, Genre, Category
from rest_framework import serializers, validators
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator 


from django.contrib.auth import get_user_model

User = get_user_model()



class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True, default=serializers.CurrentUserDefault())
    

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('author', 'title')
        #validators = [
            #UniqueTogetherValidator(
               # queryset=Review.objects.all(),
               # fields=('author', 'title'),
               # message="Возможен только один отзыв!"
           # )
       # ]

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
        rating = Review.objects.values('title_id').annotate(rating=Avg('score'))[0]['rating']
        return round(rating, 1)
    

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

