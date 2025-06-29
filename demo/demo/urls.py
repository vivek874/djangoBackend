from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from myapp.views import StudentViewSet,MarkViewSet,HomeworkViewSet,SubjectViewSet,LeaveViewSet, TeacherViewSet, RoutineViewSet

router = routers.DefaultRouter()       #url generator for my api. auto create restful api endpoints
router.register(r'students', StudentViewSet)
router.register(r'marks', MarkViewSet)
router.register(r'homework',HomeworkViewSet)
router.register(r'subjects',SubjectViewSet)
router.register(r'leaves',LeaveViewSet)
router.register(r'teachers',TeacherViewSet)
router.register(r'daily_routines',RoutineViewSet)

urlpatterns = [
  
    path("admin/", admin.site.urls),
    path("",include("myapp.urls")),
    path('api/', include(router.urls)),
   
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

