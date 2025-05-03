# train_model.py
import joblib
from myapp.utils.analysis import prepare_regression_data
from sklearn.linear_model import LinearRegression
from sklearn.metrics import  r2_score

def train_and_save_model(x_fields, y_field, subject_name, grade, section):
    X, y, _ = prepare_regression_data(
        x_fields=x_fields,
        y_field=y_field,
        subject_name=subject_name,
        grade=grade,
        section=section
    )

    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, 'trained_model.pkl')
    print("Model trained and saved successfully.")

    intercept = model.intercept_
    coefficients = {field: coef for field, coef in zip(x_fields, model.coef_)}

    # Optional: make predictions and show a sample
    predictions = model.predict(X)
    actuals = y.tolist()

  
    r2 = r2_score(y, predictions)

    print("Sample predictions:", predictions[:5])
    print("Actual values:", y[:5].tolist())
  
    print("R² Score:", r2)
    return intercept, coefficients, predictions.tolist(), actuals

if __name__ == '__main__':
    train_and_save_model()