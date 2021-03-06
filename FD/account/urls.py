from django.urls import path
from django.conf.urls import include, url
from . import views


urlpatterns = [
    url('regist_user', views.RegistUser.as_view(), name='regist_user'),
    url('app_login', views.AppLogin.as_view(), name='app_login'),
    url('profile_meal', views.ProfileMeal.as_view(), name='profile_meal'),
    url('community_img', views.CommunityImg.as_view(), name='community_img'),
    url('detect', views.Detect.as_view(), name='detect'),
    url('food_nutrition', views.FoodNutrition.as_view(), name='food_nutrition'),
    url('meal_add', views.MealAdd.as_view(), name='meal_add'),
    url('user_date_info', views.UserDateInfo.as_view(), name='user_date_info'),
    url('like', views.Like.as_view(), name='like'),
    url('user_gcode_update',views.UserGcodeUpdate.as_view(), name='user_gcode_update'),
    url('search_food',views.SearchFood.as_view(), name='search_food')
]