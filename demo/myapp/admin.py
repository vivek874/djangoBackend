from django.contrib import admin
from .models import Student

# Define a custom ModelAdmin class
class StudentAdmin(admin.ModelAdmin):
    # Define the fields to display in the list view
    list_display = ('id', 'name', 'age', 'gender', 'grade', 'section')

    # Add filters for easier searching
    list_filter = ('gender', 'grade', 'section')

    # Add search functionality to the list view
    search_fields = ('name', 'id')

    # Control the order of records
    ordering = ('name',)  # Orders by name, ascending by default

    # Add pagination (if you have many records)
    list_per_page = 20

    # Show editable fields directly in the list view (instead of requiring you to go into the details)
    list_editable = ('age', 'grade', 'section')  # These fields can be edited directly in the list view

    # Enable inlines for related models if needed
    # inlines = [StudentInline]  # Uncomment if you have related models

# Register the model with the custom admin
admin.site.register(Student, StudentAdmin)
