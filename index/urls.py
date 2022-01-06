from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup.as_view(), name='signup'),
    path('change/', views.change.as_view(), name='change'),
]