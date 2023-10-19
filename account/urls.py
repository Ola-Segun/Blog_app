from django.urls import path
from . import views

urlpatterns = [
   path('', views.droppage, name='droppage'), 
   path('login/', views.loginUser, name='login'), 
   path('logout/', views.logoutUser, name='logout'), 
   path('register/', views.registerUser, name='register'), 
]