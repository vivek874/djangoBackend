import joblib
import pandas as pd

def load_model(path='model.pkl'):
    return joblib.load(path)

def predict(input_dict):
    model = load_model()
    df = pd.DataFrame([input_dict])
    
    # Apply same normalization as training
    normalization = {
        'attendance': 200,
        'test_score': 15,
        'homework_score': 10,
        'final_score': 75,
    }
    for key in df.columns:
        if key in normalization:
            df[key] = df[key] / normalization[key]
    
    return model.predict(df)[0]