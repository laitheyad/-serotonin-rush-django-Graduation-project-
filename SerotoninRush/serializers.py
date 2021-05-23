from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'phone', 'avatar','status']

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['pk', 'img', 'name', 'fats', 'protein', 'carbohydrate', 'recipe']

class UserReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReaction
        fields = ['pk', 'user', 'meal', 'date', 'reaction']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['pk', 'title', 'body', 'url', 'image']
