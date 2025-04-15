import os
import csv
import django
import sys
sys.path.append('/Users/vivekdahal/backend/demo')  



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings') 
django.setup()

from myapp.models import Student

def load_students_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=',')
        for row in reader:

            Student.objects.create(
                id=int(row['ID']),
                name=row['Name'], 
                age=int(row['Age']),
                gender=row['Gender'],
                grade=int(row['Grade']),
                section=row['Section'],
                attendance=float(row['Attendance (%)']),
                test_score=float(row['Test Score']),
                homework_score=float(row['Homework Score']),
                final_score=float(row['Final Score'])
            )
    print("Successfully imported student data from:", csv_file_path)

if __name__ == '__main__':
    csv_path = os.path.expanduser("/Users/vivekdahal/Downloads/sample.csv")  
    load_students_from_csv(csv_path)
