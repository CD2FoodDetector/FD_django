#from django.shortcuts import render
from .models import *
from .serializers import *

# API view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .tokens import create_token, validate_token

from account.yolov5.detect import run

import datetime

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
        date = request.data.get('date', "") # 211204 추가 - 특정 날짜에 올린 사진 반환 (date필드 없으면 모든 날짜)
        ret = validate_token(token)
        if ret == True:
            imgs = []
            dt = [] # datetime
            
            if date: # date가 주어지는 경우 (ex. yyyy-mm-dd )
                y, m, d = date.split("-")
                imgs_queryset = Meal.objects.filter(user_id=id, log_time__date=datetime.date(int(y), int(m), int(d)))
            else:   # date 주어지지 않는 경우 - 모든 날짜
                imgs_queryset = Meal.objects.filter(user_id=id)
            
            imgs_queryset = list(imgs_queryset)
            imgs_queryset.sort(key=lambda x: x.log_time)
            for m in imgs_queryset:
                imgs.append(m.image_name)
                hour = int(str(m.log_time)[11:13])
                if hour < 10:
                    dt.append(0) # 아침
                elif hour < 14:
                    dt.append(1) # 점심
                else:
                    dt.append(2) # 저녁
                
            return Response({"datetime": dt, "img": imgs, "status_code": 1})
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
            imgs_list = [] # Meal object의 리스트
            for user in users: # 해당 gcode를 갖는 유저에 대해
                imgs_queryset = Meal.objects.filter(user_id=user.id) # 그 유저가 올린 식단을 리스트에 추가
                for e in list(imgs_queryset):
                    imgs_list.append(e)
            
            imgs_list.sort(key=lambda x: x.log_time)
            imgs = [] # 최종 반환할 이미지 리스트
            dt = [] # 시간
            user_id = [] # 사용자 아이디
            try:
                for m in imgs_list:
                    dt.append(str(m.log_time)[:-9])
                    user_id.append(m.user_id)
                    imgs.append(m.image_name)
                print(dt, user_id, imgs)
            except:
                pass
            return Response({"img": imgs, "status_code": 1, "user_id": user_id, "datetime": dt})
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
            results = run(imgsz=416, conf_thres=0.2, source=img_path) # yolo5.detect.run
            new_result = []
            for result in results:
                food = dict()
                food["coordinate"] = list(map(float, result[0]))
                food["p"] = float(result[1])
                food["food_id"] = result[2]
                food["food_name"] = result[3]
                new_result.append(food)
            return Response({"status_code": 1, "result": new_result})
        elif ret == "expiredSignature":
            return Response({"msg": "token expired", "status_code": 2})
        elif ret == "invalid":
            return Response({"msg": "invalid token", "status_code": 3})


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
            nu = []
            for key,value in serializer.data.items():
                nu.append({"key":key,"value": float(value)*size})
            return Response({"nutrition":nu,"id": id,"name":name, "status_code": 1})


class MealAdd(APIView):
    # Meal
    # require : totalNutritionList(key, value), image_name
    def post(self, request):
        user_id = request.data.get('id',"")
        #meal_id 결정
        meal_id = Meal.objects.filter(user=user_id).count()+1
        user = User.objects.get(id=user_id)
        #log_time
        log_time = str(datetime.datetime.now())

        calories_total = request.data.get('calories_total',"")
        carbo_total = request.data.get('carbo_total', "")
        protein_total = request.data.get('protein_total', "")
        fat_total = request.data.get('fat_total', "")
        sugar_total = request.data.get('sugar_total', "")
        salt_total = request.data.get('salt_total', "")
        saturated_fat_total = request.data.get('saturated_fat_total', "")

        image_name = request.data.get('image_name', "")

        new_meal = Meal(id=meal_id, user=user, calories_total=calories_total, carbo_total = carbo_total, protein_total = protein_total, fat_total = fat_total, sugar_total = sugar_total, salt_total = salt_total, saturated_fat_total = saturated_fat_total, log_time = log_time,image_name = image_name, public_avail = 0)
        new_meal.save()

        return Response({"status_code":1, "meal_id": new_meal.id})


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
            #info['image_name'] = meal.image_name

            infoList.append(info)
        res = {"infoList" :infoList, "infoNum": len(infoList)}

        #목표 칼로리 탄단지
        user = User.objects.filter(id = user_id).first()
        res['user_calorie'] = user.calorie
        res['user_carbo'] = user.carbohydrate
        res['user_fat'] = user.fat
        res['user_protein'] = user.protein

        return Response(res)

class Like(APIView):
    def post(self, request):
        token = request.data.get('token', "")
        uid = request.data.get('id', "")
        meal = request.data.get('meal_id', "")
        meal_user = request.data.get('meal_user_id', "")
        
        
        ret = validate_token(token)
        if ret == True:
            logtime = str(datetime.datetime.now())
            #id = User.objects.filter(id=uid).first()
            #muid = User.objects.filter(id=meal_user).first()
            #meal = Meal.objects.filter(id=meal, user=muid).first()
            id = User.objects.get(id=uid)
            muid = User.objects.get(id=meal_user)
            meal = Meal.objects.get(id=meal, user=muid)
            
            new_like = Likes(id=id, meal=meal, meal_user=meal, log_time=logtime)
            #new_like = Likes(id=id, meal=meal.id, meal_user=meal.user, log_time=logtime)
            print(new_like)
            #Likes.objects.create(id=id.id, meal=meal.id, meal_user=meal.user, log_time=logtime)
            new_like.save()
            return Response({"status_code": 1})
        elif ret == "expiredSignature":
            return Response({"msg": "token expired", "status_code": 2})
        elif ret == "invalid":
            return Response({"msg": "invalid token", "status_code": 3})


class UserGcodeUpdate(APIView):
    def post(self, request):
        id = request.data.get('id', "")
        new_gcode = request.data.get('gcode',"")

        user = User.objects.filter(id=id).first()
        user.gcode = new_gcode
        user.save()

        return Response({"gcode": user.gcode, "status_code": 1})