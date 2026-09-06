from flask import Flask, request, jsonify, Response
import joblib
import pandas as pd
import logging
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

logging.basicConfig(
    filename="model_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

model = joblib.load("churn_model.pkl")

FEATURES = [
    "age",
    "income",
    "purchases",
    "website_visits",
    "purchase_per_visit"
]

prediction_counter = Counter(
    "churn_predictions_total",
    "Total number of churn predictions",
    ["prediction"]
)

prediction_latency = Histogram(
    "churn_prediction_seconds",
    "Time spent processing churn predictions"
)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "DDS8530 Churn Prediction API",
        "status": "running",
        "monitoring": "Prometheus enabled"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        with prediction_latency.time():
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

        prediction_counter.labels(
            prediction=str(prediction)
        ).inc()

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


@app.route("/metrics", methods=["GET"])
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    print("Starting DDS8530 Machine Learning REST API...")
    print("Prometheus metrics available at http://127.0.0.1:5000/metrics")
    app.run(host="127.0.0.1", port=5000)