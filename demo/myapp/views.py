from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib import messages
from .models import CustomUser,Student
from rest_framework import viewsets
from .serializers import StudentSerializer



@api_view(["GET"])
def get_users(request):
    users = CustomUser.objects.all().values( "username", "role")
    return Response(users, status=status.HTTP_200_OK)

@api_view(["DELETE"])
def delete_user(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def register(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    role = data.get("role") 
    
    if not role or role not in dict(CustomUser.ROLE_CHOICES):
        return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.create_user(username=username, password=password, role=role)
 
    user.save()

    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def login(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
 
   
    
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    
    if role and user.role != role:
        
        return Response({"error": "Access denied: incorrect role"}, status=status.HTTP_403_FORBIDDEN)
    

    return Response({"message": "Login successful", "username": user.username, "role": user.role}, status=status.HTTP_200_OK)



 
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

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer