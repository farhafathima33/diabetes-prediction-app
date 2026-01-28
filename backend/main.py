from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load ML model
with open("../diabetes_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/", methods=["GET"])
def home():
    return "Backend is running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = np.array([[
        data["Pregnancies"],
        data["Glucose"],
        data["BloodPressure"],
        data["SkinThickness"],
        data["Insulin"],
        data["BMI"],
        data["DiabetesPedigreeFunction"],
        data["Age"]
    ]])

    prediction = model.predict(features)[0]

    return jsonify({
        "prediction": int(prediction)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
