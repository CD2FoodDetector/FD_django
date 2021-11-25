from .models import User
from rest_framework import serializers

class UserRegistSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserLoginSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','passwd']
