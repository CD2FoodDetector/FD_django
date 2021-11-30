from .models import *
from rest_framework import serializers
import datetime
import random

class UserRegistSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MealSerizlizer(serializers.ModelSerializer):
    id = random.randint(0,1<<32-1)
    class Meta:
        model = Meal
        fields = '__all__'


class LikeSerizlizer(serializers.ModelSerializer):
    log_time = datetime.datetime.now()
    class Meta:
        model = Likes
        fields = '__all__'

class FoodNutritionSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Food
        #fields = '__all__'
        exclude = ['id','food_name','serving_size_unit','serving_size']