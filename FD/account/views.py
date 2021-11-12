#from django.shortcuts import render
from .models import User, Meal
from .serializers import UserRegistSerizlizer
from .serializers import UserLoginSerizlizer
# API view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

import json
#from rest_framework_simplejwt.tokens import RefreshToken
from .tokens import create_token
from .tokens import validate_token


class AppLogin(APIView):
    def post(self, request):
        #serializer = UserLoginSerizlizer(data=request.data)
        #if serializer.is_valid():
            #db와 비교
        id = request.data.get('id',"")
        passwd = request.data.get('passwd',"")
        user = User.objects.filter(id=id).first()
      #  print("============jwt start==============")
#        refresh = RefreshToken.for_user(user)
        if user is None:
            return Response({"status_code": 2, "msg": "ID가 없습니다."})
        if user.passwd != passwd:
            return Response({"status_code": 3, "msg": "비밀번호가 틀렸습니다."})
        else:
            return Response({"status_code": 1, "token": create_token(id),"msg": "로그인 성공"})
        #id, pw 비교후 응답
       # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistUser(APIView):
    def post(self, request):
       serializer = UserRegistSerizlizer(data = request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)

       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileMeal(APIView):
    def post(self, request):
        token = request.data.get('token', "")
        id = request.data.get('id',"")
        ret = validate_token(token)
        if ret == True:
            imgs_queryset = Meal.objects.filter(user_id=id)
            imgs = []
            for m in imgs_queryset:
                imgs.append(m.image_name)
            print(imgs)
            return Response({"img": imgs})
        elif ret == "expiredSignature":
            return Response({"msg": "token expired"})
        elif ret == "invalid":
            return Response({"msg": "invalid token"})