import pandas as pd
from sklearn.linear_model import LinearRegression
from myapp.models import Student, Mark,Subject



def load_and_merge_data():
    # Load student data
    s_qs = Student.objects.filter(academic_year='2024').values('academic_year', 'id','name', 'grade', 'section', 'attendance','final_aggregate')
    s_df = pd.DataFrame(list(s_qs))

    # Load mark data
    m_qs = Mark.objects.select_related('student', 'subject').values(
        'student_id', 'subject_id', 'test_score', 'homework_score', 'final_score', 'aggregate',
    )
    m_df = pd.DataFrame(list(m_qs))

    # Merge the two DataFrames on student ID
    merged_df = pd.merge(m_df, s_df, left_on='student_id', right_on='id', how='inner')

    return s_df, m_df, merged_df

def prepare_regression_data(
    x_fields=['attendance'], 
    y_field='aggregate', 
    subject_name=None, 
    grade=None, 
    section=None
):
    # Load and merge data
    s_df, m_df, merged_df = load_and_merge_data()

    # Create subject ID → name map
    subject_map = {s.id: s.name for s in Subject.objects.all()}
    merged_df['subject_name'] = merged_df['subject_id'].map(subject_map)

    # Optional filters
    if subject_name is not None:
        merged_df = merged_df[merged_df['subject_name'] == subject_name]
    if grade is not None:
        merged_df = merged_df[merged_df['grade'] == grade]
    if section is not None:
        merged_df = merged_df[merged_df['section'] == section]

    # Drop rows with missing values in selected fields
    required_fields = x_fields + [y_field]
    merged_df = merged_df.dropna(subset=required_fields)

    # Prepare features (X) and target (y)
    X = merged_df[x_fields]
    y = merged_df[y_field]
  

    # Normalize fields to bring them on comparable scales
    normalization_factors = {
        'attendance': 200.0,
        'test_score': 15.0,
        'homework_score': 10.0,
        'final_score': 75.0,
        'aggregate': 100.0,
    }

    for col in X.columns:
        if col in normalization_factors:
            X.loc[:, col] = X[col] / normalization_factors[col]

    if y.name in normalization_factors:
        y = y / normalization_factors[y.name]

    return X, y, merged_df

