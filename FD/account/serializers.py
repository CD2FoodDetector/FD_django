from .models import User, Likes, Food
from rest_framework import serializers
import datetime

class UserRegistSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LikeSerizlizer(serializers.ModelSerializer):
    log_time = datetime.datetime.now()
    class Meta:
        model = Likes
        fields = '__all__'

class FoodNutritionSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'
        exclude = ['id','food_name']