import joblib
import pandas as pd
import os

def load_model(path):
    return joblib.load(path)

def predict(input_dict, subject_name, grade, y_field,x_fields):
    # Construct model path
    model_path = f'models/model_{subject_name}_grade{grade}_{y_field}_{x_fields}.pkl'
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    
    model = load_model(model_path)
    df = pd.DataFrame([input_dict])

    normalization = {
        'attendance': 200,
        'test_score': 15,
        'homework_score': 10,
        'final_score': 75,
    }

    for key in df.columns:
        if key in normalization:
            df[key] = df[key] / normalization[key]

    return float(model.predict(df)[0])


def predict_batch(students_data, subject_name, grade, y_field, x_fields):
    model_path = f'models/model_{subject_name}_grade{grade}_{y_field}_{x_fields}.pkl'
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

    model = load_model(model_path)

    df = pd.DataFrame(students_data)

    normalization = {
        'attendance': 200,
        'test_score': 15,
        'homework_score': 10,
        'final_score': 75,
    }

    for field in x_fields:
        if field in normalization and field in df.columns:
            df[field] = df[field] / normalization[field]

    X = df[x_fields]

    predictions = model.predict(X)
    df['prediction'] = predictions

    return df[['student_id', 'student_name', 'prediction']].to_dict(orient='records')