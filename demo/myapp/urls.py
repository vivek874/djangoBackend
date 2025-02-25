from django.urls import path
from . import views

urlpatterns = [
  
   
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
     path("create-user/", views.create_user_view, name="create-user"),
 
    
]

