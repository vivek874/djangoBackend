from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib import messages
from .models import CustomUser,Student,Mark,Subject,Homework,Leave, Teacher
from rest_framework import viewsets
from .serializers import StudentSerializer,MarkSerializer,SubjectSerializer,HomeworkSerializer,LeaveSerializer, TeacherSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout


# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data.get('username')
#         password = data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)  # Uses session-based login
#             return JsonResponse({
#                 'success': True,
#                 'role': user.groups.first().name if user.groups.exists() else 'user'
#             })
#         else:
#             return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
        
# @csrf_exempt
# def logout_view(request):
#     logout(request)
#     return JsonResponse({'success': True})


# API to get and delete users in admin page
@api_view(["GET"])
def get_users(request):
    users = CustomUser.objects.all().values( "username", "role")
    return Response(users, status=status.HTTP_200_OK)

@api_view(["DELETE"])
def delete_user(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)



# role assignment during login
@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role") 
    
    if not role or role not in dict(CustomUser.ROLE_CHOICES):
        return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.create_user(username=username, password=password, role=role)
 
    user.save()

    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)



@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role")
    
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if role and user.role != role:
        return Response({"error": "Access denied: incorrect role"}, status=status.HTTP_403_FORBIDDEN)
    
    return Response({"message": "Login successful", "username": user.username, "role": user.role}, status=status.HTTP_200_OK)


 #assign mark for indivisual subjects
@api_view(["POST"])
def assign_mark(request):
    data = request.data

    try:
        student_id = data.get("student_id")
        subject_name = data.get("subject")
        assign_to = data.get("assign_to")  # test_score, homework_score, final_exam
        score = data.get("score")

        if not all([student_id, subject_name, assign_to, score is not None]):
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.get(id=student_id)
        subject, _ = Subject.objects.get_or_create(name=subject_name)

        # Try to get an existing Mark or create new
        mark, created = Mark.objects.get_or_create(student=student, subject=subject, defaults={
            "test_score": 0,
            "homework_score": 0,
            "final_score": 0,
        })

        if assign_to == "test_score":
            mark.test_score = score
        elif assign_to == "homework_score":
            mark.homework_score = score
        elif assign_to == "final_exam":
            mark.final_score = score
        else:
            return Response({"error": "Invalid assign_to value"}, status=status.HTTP_400_BAD_REQUEST)

        mark.save()
        return Response({"message": "Mark assigned successfully"}, status=status.HTTP_200_OK)

    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#function for html form user creation 
def create_user_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")  
        
        if not role or role not in dict(CustomUser.ROLE_CHOICES):
            messages.error(request, "Invalid role selected.")
            return redirect("create-user")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            user = CustomUser.objects.create_user(username=username, password=password)
            user.role = role
            user.save()
            messages.success(request, f"User {user.username} created successfully!")
            return redirect("create-user")  # Redirect to the same form after creation

    return render(request, "create_user.html")

#api for homework
@api_view(["POST"])
def assign_homework(request):
    title = request.data.get("title")
    class_name = request.data.get("class_name")
    section = request.data.get("section")
    subject = request.data.get("subject")
    due_date = request.data.get("due_date")  # optional

    if not title or not class_name or not section or not subject:
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    homework = Homework.objects.create(
        title=title,
        class_name=class_name,
        section=section,
        subject=subject,
        due_date=due_date
    )
    homework.save()

    return Response({"message": "Homework assigned successfully!"}, status=status.HTTP_201_CREATED)


#viewsets
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    @action(detail=True, methods=['get'])
    def marks(self, request, pk=None):
      student = self.get_object()
      marks = Mark.objects.filter(student=student)
      serializer = MarkSerializer(marks, many=True)
      return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        attendance_increment = request.data.get("add_attendance")

        if attendance_increment is not None:
            try:
                attendance_increment = int(attendance_increment)
                instance.attendance += attendance_increment
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            except ValueError:
                return Response({"error": "Invalid attendance increment."}, status=status.HTTP_400_BAD_REQUEST)

        # Fallback to default behavior for other updates
        return super().partial_update(request, *args, **kwargs)
    
    
    def get_queryset(self):
        queryset = Student.objects.all()
        grade = self.request.query_params.get('grade')
        section = self.request.query_params.get('section')
        subject_name = self.request.query_params.get('subject')
        test_score=self.request.query_params.get('test_score')
        homework_score=self.request.query_params.get('homework_score')
        final_exam=self.request.query_params.get('final_exam')

        if grade:
            queryset = queryset.filter(grade=grade)
        if section:
            queryset = queryset.filter(section=section)
        if subject_name:
            queryset = queryset.filter(marks__subject__name=subject_name).distinct()
        if test_score :
             queryset = queryset.filter(test_score=test_score)
        if homework_score :
             queryset = queryset.filter(homework_score=homework_score)
        if final_exam :
             queryset = queryset.filter(final_exam=final_exam)


        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['subject'] = self.request.query_params.get('subject')
        return context


    
class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    
class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    
