from django.contrib import admin
from django.urls import path, include
from myapp import views

from rest_framework import routers
from myapp.views import StudentViewSet,MarkViewSet,HomeworkViewSet,SubjectViewSet,LeaveViewSet, TeacherViewSet

router = routers.DefaultRouter()       #url generator for my api. auto create restful api endpoints
router.register(r'students', StudentViewSet)
router.register(r'marks', MarkViewSet)
router.register(r'homework',HomeworkViewSet)
router.register(r'subjects',SubjectViewSet)
router.register(r'leaves',LeaveViewSet)
router.register(r'teachers',TeacherViewSet)

urlpatterns = [
  
    path("admin/", admin.site.urls),
    path("",include("myapp.urls")),
    path('api/', include(router.urls))
    
]
