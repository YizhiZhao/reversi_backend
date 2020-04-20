from django.urls import path
from . import views

urlpatterns = [
    path('nextmove', views.nextmove, name='nextmove'),
]