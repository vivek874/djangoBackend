from django.core.management.base import BaseCommand
from myapp.models import Student, Subject, Mark
import os
import django
import sys
import random

# Step 1: Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Step 2: Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')  # use your project name here

# Step 3: Setup Django
django.setup()

# Step 4: Now import your models
from myapp.models import Student, Subject, Mark

# (rest of your script remains the same)
class Command(BaseCommand):
    help = 'Fill student data with sample marks and attendance'

    def handle(self, *args, **kwargs):
        subjects = ['Nepali', 'English', 'Math', 'Science']

        for student in Student.objects.all():
            # Assign random attendance between 100 and 200 days
            student.attendance = random.randint(100, 200)
            student.save()

            for subject_name in subjects:
                subject, _ = Subject.objects.get_or_create(name=subject_name)

                # Use attendance to influence scores: higher attendance = higher marks
                attendance_factor = student.attendance / 200.0  # Normalize to 0–1

                # Homework score influenced by attendance
                homework_score = min(random.uniform(4, 8) + (0.3 * attendance_factor), 10)

                # Test score influenced by attendance and homework
                test_score = min(random.uniform(7, 12) + (0.5 * homework_score) + (0.3 * attendance_factor), 15)

                # Final score depends on test, homework, and attendance
                final_score = min((test_score * 1.1) + (homework_score * 1.2) + (attendance_factor * 10), 75)

                # Slight recomputation for tighter dependency loop
                test_score = min(test_score + 0.05 * final_score, 15)
                homework_score = min(homework_score + 0.05 * final_score, 10)
                final_score = min((test_score * 1.1) + (homework_score * 1.2) + (attendance_factor * 10), 75)

                # Calculate weighted aggregate
                aggregate = (test_score * 0.15) + (homework_score * 0.10) + (final_score * 0.75)

                Mark.objects.update_or_create(
                    student=student,
                    subject=subject,
                    defaults={
                        'test_score': round(test_score, 2),
                        'homework_score': round(homework_score, 2),
                        'final_score': round(final_score, 2),
                        'aggregate': round(aggregate, 2)
                    }
                )

        self.stdout.write(self.style.SUCCESS('Student data filled successfully.'))