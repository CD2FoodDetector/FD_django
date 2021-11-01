from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url('regist_user', views.RegistUser.as_view(), name='regist_user'),
    url('app_login', views.AppLogin.as_view(), name='app_login'),
    url('profile_meal', views.ProfileMeal.as_view(), name='profile_meal'),
]