from django.core.management.base import BaseCommand
from myapp.models import Student, Subject, Mark
import os
import django
import sys
import random


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')  


django.setup()


from myapp.models import Student, Subject, Mark


class Command(BaseCommand):
    help = 'Fill student data with sample marks and attendance'

    def handle(self, *args, **kwargs):
        subjects = ['Nepali', 'English', 'Maths', 'Science','Health','Computer','Social']

        for student in Student.objects.filter(academic_year="2024"):
            # Assign random attendance between 100 and 200 days
            student.attendance = random.randint(100, 200)
            student.save()

            for subject_name in subjects:
                subject, _ = Subject.objects.get_or_create(name=subject_name)

                # Using attendance to influence scores
                attendance_factor = student.attendance / 200.0  # Normalize to 0–1

                # Homework score influenced by attendance
                homework_score = min(random.uniform(4, 8) + (0.6 * attendance_factor), 10)

                # Test score influenced by attendance and homework
                test_score = min(random.uniform(7, 12) + (0.5 * homework_score) + (0.6 * attendance_factor), 15)

                # Final score depends on test, homework, and attendance
                final_score = min((test_score * 1.6) + (homework_score * 1.4) + (attendance_factor * 10), 75)

                # Slight recomputation for tighter dependency loop
                test_score = min(test_score + 0.05 * final_score, 15)
                homework_score = min(homework_score + 0.05 * final_score, 10)
                final_score = min((test_score * 1.6) + (homework_score * 1.4) + (attendance_factor * 10), 75)

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