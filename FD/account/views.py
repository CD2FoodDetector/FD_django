#from django.shortcuts import render
from .models import *
from .serializers import *
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

class AddLikes(APIView):
    def post(self,request):
        token = request.data.get('token', "")
        meal_id = request.data.get('meal',"")
        meal_user_id = request.data.get('meal_user_id',"")
        like_user_id = request.data.get('id', "")
        ret = validate_token(token)
        if ret == True:
            meal = Meal.objects.filter(id= meal_id, user = meal_user_id).first()
            user = User.objects.filter(id=like_user_id).first()
            if meal is None or user is None:
                return Response({"msg": "id error", "status_code": 4})

            serializer = LikeSerizlizer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "success", "status_code": 1})

            return Response({"data": serializer.errors, "status_code": 5})


        elif ret == "expiredSignature":
            return Response({"msg": "token expired", "status_code": 2})
        elif ret == "invalid":
            return Response({"msg": "invalid token", "status_code": 3})
        return Response({"msg": "unknown error", "status_code": 6})

class FoodNutrition(APIView):
    def post(self, request):
        id = request.data.get('id',"")
        food = Food.objects.filter(id=id).first()
        size = float(request.data.get('size',""))
        size_unit = request.data.get('size_unit',"")
        if food is None:
            return Response({"status_code": 2, "msg": "음식 DB에 없습니다."})
        else:
            name = food.food_name
            serializer = FoodNutritionSerizlizer(food)
            for key,value in serializer.data.items():
                serializer.data[key] = float(value)/size
            return Response({"nutrition":serializer.data,"id": id,"name":name, "status_code": 1})


class MealAdd(APIView):
    def post(self, request):
        # 밀 등록
       serializer = MealSerizlizer(data = request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)

       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDateInfo(APIView):
    def post(self, request):
        #date form : yyyy-mm-dd
        target_date = request.data.get('date', "")
        user_id = request.data.get('id', "")

        # 로그인을 했으므로 딱히 user id check x

        meals = Meal.objects.filter(user = user_id, log_time__date = target_date)\
            .order_by('log_time')
        infoList = []
        for meal in meals:

            info = {}
            info['calories_total'] = meal.calories_total
            info['carbo_total'] = meal.carbo_total
            info['fat_total'] = meal.fat_total
            info['protein_total'] = meal.protein_total
            info['image_name'] = meal.image_name

            infoList.append(info)
        res = {"infoList" :infoList, "infoNum": len(infoList)}

        #목표 칼로리 탄단지
        user = User.objects.filter(id = user_id).first()
        res['user_calorie'] = user.calorie
        res['user_carbo'] = user.carbohydrate
        res['user_fat'] = user.fat
        res['user_protein'] = user.protein

        return Response(res)
