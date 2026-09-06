import pandas as pd
import mlflow
import mlflow.sklearn
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("Starting MLflow experiment tracking...")

# Load processed data
df = pd.read_csv("processed_data.csv")

features = [
    "age",
    "income",
    "purchases",
    "website_visits",
    "purchase_per_visit"
]

X = df[features]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

# Configure MLflow experiment
mlflow.set_experiment("DDS8530_Churn_Prediction")

with mlflow.start_run():

    # Model parameters
    n_estimators = 100
    max_depth = 5

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # Track parameters
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("test_size", 0.30)

    # Track performance
    mlflow.log_metric("accuracy", accuracy)

    # Track trained model
    mlflow.sklearn.log_model(
        model,
        name="churn_model"
    )

    joblib.dump(model, "churn_model_mlflow.pkl")

    print(f"Experiment: DDS8530_Churn_Prediction")
    print(f"n_estimators: {n_estimators}")
    print(f"max_depth: {max_depth}")
    print(f"Model accuracy: {accuracy:.2%}")
    print("Parameters and metrics logged to MLflow.")
    print("MLFLOW TRACKING COMPLETED SUCCESSFULLY")