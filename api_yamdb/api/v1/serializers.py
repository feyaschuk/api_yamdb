from reviews.models import Comment, Review, User
from rest_framework import serializers, validators


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Comment    


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
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
