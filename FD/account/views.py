#from django.shortcuts import render
from .models import User, Meal
from .serializers import UserRegistSerizlizer
# API view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

import json
from .tokens import create_token, validate_token

from account.yolov5.detect import run


class AppLogin(APIView):
    def post(self, request):
        id = request.data.get('id',"")
        passwd = request.data.get('passwd',"")
        user = User.objects.filter(id=id).first()
        if user is None:
            return Response({"status_code": 2, "msg": "ID가 없습니다."})
        if user.passwd != passwd:
            return Response({"status_code": 3, "msg": "비밀번호가 틀렸습니다."})
        else:
            return Response({"status_code": 1, "token": create_token(id),"msg": "로그인 성공"})


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
            return Response({"img": imgs, "status_code": 1})
        elif ret == "expiredSignature":
            return Response({"msg": "token expired", "status_code": 2})
        elif ret == "invalid":
            return Response({"msg": "invalid token", "status_code": 3})
        
        
class CommunityImg(APIView):
    def post(self, request):
        token = request.data.get('token', "")
        gcode_ = request.data.get('gcode',"")
        
        ret = validate_token(token)
        if ret == True:
            users = User.objects.filter(gcode=gcode_)
            for user in users:
                imgs_queryset = Meal.objects.filter(user_id=user.id)
            imgs = []
            try:
                for m in imgs_queryset:
                    imgs.append(m.image_name)
            except:
                pass
            return Response({"img": imgs, "status_code": 1})
        elif ret == "expiredSignature":
            return Response({"msg": "token expired", "status_code": 2})
        elif ret == "invalid":
            return Response({"msg": "invalid token", "status_code": 3})
        

class Detect(APIView):
    def post(self, request):
        token = request.data.get('token', "")
        img_name = request.data.get('img_name', "")  # ex. 1.jpg
        img_path = "http://3.36.103.81/images/" + img_name  # nginx server path
        
        ret = validate_token(token)
        if ret == True:
            result = run(imgsz=416, conf_thres=0.2, source=img_path) # yolo5.detect.run
            return Response({"status_code": 1, "result": result})
        elif ret == "expiredSignature":
            return Response({"msg": "token expired", "status_code": 2})
        elif ret == "invalid":
            return Response({"msg": "invalid token", "status_code": 3})