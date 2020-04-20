from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('exit', views.exit, name='exit'),
    path('userdata', views.userdata, name='userdata'),
]