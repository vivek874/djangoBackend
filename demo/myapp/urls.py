from django.urls import path
from . import views



urlpatterns = [
  
   
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path("users/", views.get_users, name="get_users"),    #this is to display existing users
    path('delete-user/<str:username>/', views.delete_user, name='delete-user'),  
    path("create-user/", views.create_user_view, name="create-user"),
    # path('api/assign-mark/', views.assign_mark, name="assign-mark"),
   
]

