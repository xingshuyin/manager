from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('loginout/', views.loginout, name='loginout'),
]