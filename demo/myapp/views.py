from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib import messages
from .models import CustomUser,Student,Mark,Subject,Homework,Leave, Teacher, DailyRoutine
from rest_framework import viewsets
from .serializers import StudentSerializer,MarkSerializer,SubjectSerializer,HomeworkSerializer,LeaveSerializer, TeacherSerializer, DailyRoutineSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    return Response({
        'username': user.username,
        'role': user.role  # assuming you have a `role` field in your CustomUser model
    })


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
    permission_classes = [IsAuthenticatedOrReadOnly]
    
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
        academic_year = self.request.query_params.get('academic_year')
        section = self.request.query_params.get('section')
        subject_name = self.request.query_params.get('subject')
        test_score=self.request.query_params.get('test_score')
        homework_score=self.request.query_params.get('homework_score')
        final_exam=self.request.query_params.get('final_exam')

        if grade:
            queryset = queryset.filter(grade=grade)
        if academic_year:
         queryset = queryset.filter(academic_year=academic_year)
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
    permission_classes = [IsAuthenticatedOrReadOnly]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        teacher, _ = Teacher.objects.get_or_create(user=self.request.user, defaults={
            "subject": "General"
        })
        serializer.save(teacher=teacher)
        
    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            return Leave.objects.all()
        
        if user.role=='admin':
            return Leave.objects.all()
        
        if user.role == 'teacher':
            
         return Leave.objects.filter(teacher__user=self.request.user)
        
        
    @action(detail=True , methods=['patch'])
    def update_status(self, request,pk=None):
        leave = self.get_object()
        status_value = request.data.get('status')
        
        if status_value not in ['approved','declined']:
            return Response({'error': 'invalid status'},status=400)
        
        leave.status = status_value
        leave.save()
        return Response ({'message':'leave{status_value}'},status = 200)
         
            
       
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class RoutineViewSet(viewsets.ModelViewSet):
    queryset = DailyRoutine.objects.all()
    serializer_class = DailyRoutineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        grade = request.data.get('grade')
        routine_file = request.FILES.get('routine')

        if not grade or not routine_file:
            return Response({"error": "Grade and routine image are required"}, status=400)

        existing = DailyRoutine.objects.filter(grade=grade).first()

        if existing:
            existing.routine = routine_file
            existing.save()
            return Response(DailyRoutineSerializer(existing).data, status=200)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=201)

    def get_queryset(self):
        queryset = DailyRoutine.objects.all()
        grade = self.request.query_params.get('grade')
        if grade:
            queryset = queryset.filter(grade=grade)
        return queryset

            
    


# Student performance 
import joblib
from myapp.utils.analysis import prepare_regression_data  # Adjust if your utils file has a different path
from django.views.decorators.http import require_GET

# This function uses a trained regression model to predict student performance and display the results in a rendered HTML template.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def student_performance_view(request):
    # Load the trained model
    model = joblib.load('trained_model.pkl')

    # Prepare data
    x, _, merged_df = prepare_regression_data()

    # Make predictions
    predictions = model.predict(x)

    # Add predictions to the DataFrame
    merged_df['predicted_score'] = predictions

    # Render the results
    return render(request, 'your_template.html', {'data': merged_df.to_dict(orient='records')})


from django.shortcuts import render
from myapp.utils.train_model import train_and_save_model  # import your training function


# passes parameters in the train_model.html
def train_model_view(request):
    if request.method == 'POST':
        x_fields = request.POST.getlist('x_fields')  # multiple input fields with same name
        y_field = request.POST.get('y_field')
        subject_name = request.POST.get('subject_name')
        grade = int(request.POST.get('grade'))

        # Capture model_path in return values
        intercept, coefficients, predictions, actuals, model_path = train_and_save_model(
            x_fields=x_fields,
            y_field=y_field,
            subject_name=subject_name,
            grade=grade,
        )

        from sklearn.metrics import r2_score
        from .models import ModelTraining

        # Calculate R² score
        r2 = r2_score(actuals, predictions)

        # Save the training results to the database, including model_path
        ModelTraining.objects.create(
            subject_name=subject_name,
            grade=grade,
            intercept=intercept,
            coefficients=dict(zip(x_fields, coefficients)),
            r2_score=r2,
            model_path=model_path
        )

        return render(request, 'train_result.html', {
            'message': 'Model trained successfully!',
            'intercept': intercept,
            'coefficients': coefficients,
            'predictions': predictions,
            'actuals': actuals,
            'r2': r2
        })

    return render(request, 'train_model.html')


from .models import ModelTraining

# View to display model training history
@api_view(["GET"])
@permission_classes([AllowAny])
def training_history_view(request):
    trainings = ModelTraining.objects.all().order_by('-date_trained')
    history = []
    for training in trainings:
        history.append({
            'date_trained': training.date_trained.strftime("%Y-%m-%d %H:%M:%S"),
            'subject_name': training.subject_name,
            'grade': training.grade,
            'intercept': training.intercept,
            'coefficients': training.coefficients,
            'r2_score': training.r2_score,
            
        })
    return Response({'training_history': history}, status=status.HTTP_200_OK)

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json
import os
import pandas as pd
import joblib


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def predict_view(request):
    try:
        data = json.loads(request.body)

        subject_name = data.get('subject_name')
        grade = data.get('grade')
        x_fields = data.get('x_fields')
        y_field = data.get('y_field')
        academic_year = data.get("academic_year")

        if not all([subject_name, grade, x_fields, y_field,academic_year]):
            return Response({'error': 'Missing required fields'}, status=400)

        x_field_str = "_".join(x_fields)
        model_path = f'models/model_{subject_name}_grade{grade}_{y_field}_{x_field_str}.pkl'
        if not os.path.exists(model_path):
            return Response({'error': f'Model not found at {model_path}'}, status=404)

        model = joblib.load(model_path)

        # Query all students in the grade
        academic_year = data.get('academic_year')
        students = Student.objects.filter(grade=grade, academic_year=academic_year)

        rows = []

        for student in students:
            try:
                mark = Mark.objects.get(student=student, subject__name=subject_name)
                row = {}
                for field in x_fields:
                    row[field] = getattr(mark, field, 0)
                row['student_id'] = student.id
                row['student_name'] = student.name
                rows.append(row)
            except Mark.DoesNotExist:
                continue

        if not rows:
            return Response({'error': 'No marks found for students'}, status=404)

        df = pd.DataFrame(rows)

        normalization = {
            'attendance': 200,
            'test_score': 15,
            'homework_score': 10,
            'final_score': 75,
        }

        for field in x_fields:
            if field in normalization:
                df[field] = df[field] / normalization[field]

        predictions = model.predict(df[x_fields])
        df['predicted_' + y_field] = predictions

        # Ensure x_fields are included in the result columns
        result = df[['student_id', 'student_name'] + x_fields + ['predicted_' + y_field]].to_dict(orient='records')

        return Response({'predictions': result}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
def health(request):
    try:
        return JsonResponse({'active'},status=200)
    except Exception as e:
        return JsonResponse({'error'},status=500)