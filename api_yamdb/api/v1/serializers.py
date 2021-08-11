from titles.models import Comment, Review, User
from rest_framework import serializers


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
