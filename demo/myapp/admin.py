from django.contrib import admin
from .models import Student, Subject, Teacher, Leave

# Define a custom ModelAdmin class for Student
class StudentAdmin(admin.ModelAdmin):
    # Define the fields to display in the list view
    list_display = ('id', 'name', 'age', 'gender', 'grade', 'section')


    # Add filters for easier searching
    list_filter = ('gender', 'grade', 'section')

    # Add search functionality to the list view
    search_fields = ('name', 'id')

    # Control the order of records
    ordering = ('id',)  # Orders by name, ascending by default

    # Add pagination (if you have many records)
    list_per_page = 10

    # Show editable fields directly in the list view
    list_editable = ('age', 'grade', 'section')  # These fields can be edited directly in the list view

 

# Register the model with the custom admin
admin.site.register(Student, StudentAdmin)



# Register the Teacher model with the custom admin
admin.site.register(Teacher)

# Register the other models
admin.site.register(Subject)
admin.site.register(Leave)
