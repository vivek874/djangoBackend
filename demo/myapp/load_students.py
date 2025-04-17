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
               
                name=row['name'], 
                age=int(row['age']),
                gender=row['gender'],
                grade=int(row['grade']),
                section=row['section'],
                attendance=float(row['attendance']),
                test_score=float(row['test_score']),
                homework_score=float(row['homework_score']),
                final_exam=float(row['final_exam']),
                aggregate = float(row['aggregate']),
              
            )
    print("Successfully imported student data from:", csv_file_path)

if __name__ == '__main__':
    csv_path = os.path.expanduser("/Users/vivekdahal/Downloads/dataset.csv")  
    load_students_from_csv(csv_path)
