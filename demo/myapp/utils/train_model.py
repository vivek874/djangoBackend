# train_model.py
import joblib
from myapp.utils.analysis import prepare_regression_data
from sklearn.linear_model import LinearRegression
from sklearn.metrics import  r2_score
import os

def train_and_save_model(x_fields, y_field, subject_name, grade):
    X, y, _ = prepare_regression_data(
        x_fields=x_fields,
        y_field=y_field,
        subject_name=subject_name,
        grade=grade,
       
    )

    model = LinearRegression()
    model.fit(X, y)

    intercept = model.intercept_
    coefficients = {field: coef for field, coef in zip(x_fields, model.coef_)}

   
    predictions = model.predict(X)
    actuals = y.tolist()

  
    r2 = r2_score(y, predictions)

    # Ensure models directory exists
    os.makedirs('models', exist_ok=True)

    # Generate a unique filename for this model
    x_field_str = "_".join(x_fields)
    model_filename = f"model_{subject_name}_grade{grade}_{y_field}_{x_field_str}.pkl"
    model_path = os.path.join("models", model_filename)

    if r2 >= 0.4:
        joblib.dump(model, model_path)
        print("Model trained and saved successfully.")
    else:
        print("Model not saved due to low R² score.")

    print("Sample predictions:", predictions[:5])
    print("Actual values:", y[:5].tolist())
  
    print("R² Score:", r2)
    return intercept, coefficients, predictions.tolist(), actuals, model_path

if __name__ == '__main__':
    train_and_save_model()