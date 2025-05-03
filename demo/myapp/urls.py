from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import student_performance_view
urlpatterns = [
   
    path('performance/', student_performance_view, name='performance'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path("users/", views.get_users, name="get_users"),    #this is to display existing users
    path('delete-user/<str:username>/', views.delete_user, name='delete-user'),  
    path("create-user/", views.create_user_view, name="create-user"),
    path('api/assign-mark/', views.assign_mark, name="assign-mark"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', views.get_current_user, name='get-current-user'),
    path('train-model/', views.train_model_view, name='train-model'),

]
