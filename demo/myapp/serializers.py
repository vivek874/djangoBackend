from rest_framework import serializers
from .models import Student, Mark,Subject,Homework,Leave,Teacher

class MarkSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Mark
        fields =  '__all__'
        
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class StudentSerializer(serializers.ModelSerializer):
    marks = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'gender', 'grade', 'section', 'attendance', 'final_aggregate','marks']

    def get_marks(self, obj):
        marks_data = {}
        # Iterate over all the marks related to the student.
        for mark in obj.marks.all():
            subject_name = mark.subject.name  # Get the subject name.
            marks_data[subject_name] = {
                'test_score': mark.test_score,
                'homework_score': mark.homework_score,
                'final_score': mark.final_score,
                'aggregate': mark.aggregate,
            }
        return marks_data

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
       model = Homework
       fields = '__all__'
       
class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'
        
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'