from flask import Flask, request, jsonify
import joblib
import pandas as pd
import logging

app = Flask(__name__)

logging.basicConfig(
    filename="model_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load trained machine learning model
model = joblib.load("churn_model.pkl")

FEATURES = [
    "age",
    "income",
    "purchases",
    "website_visits",
    "purchase_per_visit"
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "DDS8530 Churn Prediction API",
        "status": "running"
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        input_data = pd.DataFrame(
            [[
                data["age"],
                data["income"],
                data["purchases"],
                data["website_visits"],
                data["purchase_per_visit"]
            ]],
            columns=FEATURES
        )

        prediction = int(model.predict(input_data)[0])

        logging.info("Prediction completed: %s", prediction)

        return jsonify({
            "prediction": prediction,
            "result": "Customer likely to churn"
            if prediction == 1
            else "Customer unlikely to churn"
        })

    except Exception as error:
        logging.error("Prediction error: %s", error)

        return jsonify({
            "error": str(error)
        }), 400

if __name__ == "__main__":
    print("Starting DDS8530 Machine Learning REST API...")
    app.run(host="127.0.0.1", port=5000)