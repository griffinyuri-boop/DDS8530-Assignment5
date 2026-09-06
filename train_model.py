import pandas as pd
import joblib
import logging

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

logging.basicConfig(
    filename="model_training.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print("Starting machine learning model training...")

# Load processed ETL data
df = pd.read_csv("processed_data.csv")

# Select model features
features = [
    "age",
    "income",
    "purchases",
    "website_visits",
    "purchase_per_visit"
]

X = df[features]
y = df["churn"]

print(f"Loaded {len(df)} processed records.")
print(f"Model features: {len(features)}")

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

print(f"Training records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")

# Create and train model
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("\nModel evaluation:")
print(f"Accuracy: {accuracy:.2%}")

print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Save trained model
joblib.dump(model, "churn_model.pkl")

print("Trained model saved as churn_model.pkl")
print("MODEL TRAINING COMPLETED SUCCESSFULLY")

logging.info("Model trained with accuracy: %.4f", accuracy)
logging.info("Trained model saved successfully.")