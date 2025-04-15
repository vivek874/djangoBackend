from django.contrib import admin
from django.urls import path, include
from myapp import views

from rest_framework import routers
from myapp.views import StudentViewSet

router = routers.DefaultRouter()       #url generator for my api. auto create restful api endpoints
router.register(r'students', StudentViewSet)

urlpatterns = [
  
    path("admin/", admin.site.urls),
    path("",include("myapp.urls")),
    path('api/', include(router.urls))
    
]
