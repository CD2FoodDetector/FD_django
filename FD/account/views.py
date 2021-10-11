#from django.shortcuts import render
from .models import User
from .serializers import UserRegistSerizlizer
from .serializers import UserLoginSerizlizer
# API view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class AppLogin(APIView):
    def post(self, request):
        #serializer = UserLoginSerizlizer(data=request.data)
        #if serializer.is_valid():
            #db와 비교
        id = request.data.get('id',"")
        passwd = request.data.get('passwd',"")
        user = User.objects.filter(id=id).first()
        if user is None:
            return Response({"status_code": 2, "msg": "ID가 없습니다."})
        if user.passwd != passwd:
            return Response({"status_code": 3, "msg": "비밀번호가 틀렸습니다."})
        else:
            return Response({"status_code": 1, "msg": "로그인 성공"})
        #id, pw 비교후 응답
       # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistUser(APIView):
    def post(self, request):
       serializer = UserRegistSerizlizer(data = request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)

       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
