from .models import User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserLoginSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','passwd']

class UserSerializerWithJWT(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()