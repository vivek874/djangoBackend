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
               
                final_aggregate = float(row['aggregate']),
              
            )
    print("Successfully imported student data from:", csv_file_path)

if __name__ == '__main__':
    csv_path = os.path.expanduser("/Users/vivekdahal/Downloads/added_dataset.csv")  
    load_students_from_csv(csv_path)
