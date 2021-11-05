from django.urls import path
from django.conf.urls import include, url
from . import views
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    url('regist_user', views.RegistUser.as_view(), name='regist_user'),
    url('app_login', views.AppLogin.as_view(), name='app_login'),
  #  path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  #  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]