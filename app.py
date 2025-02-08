from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load models
with open("irrigation_model.pkl", "rb") as f:
    model_irrigation = pickle.load(f)
with open("health_model.pkl", "rb") as f:
    model_health = pickle.load(f)

# Crop encoding
crop_mapping = {'Wheat': 0, 'Rice': 1, 'Corn': 2, 'Soybean': 3, 'Cotton': 4}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        soil_moisture = float(request.form['soil_moisture'])
        rainfall = float(request.form['rainfall'])
        crop_type = request.form['crop_type']

        if crop_type not in crop_mapping:
            return "Invalid crop type"
        
        crop_type_encoded = crop_mapping[crop_type]
        input_features = np.array([[temperature, humidity, soil_moisture, rainfall, crop_type_encoded]])

        irrigation_prediction = model_irrigation.predict(input_features)[0]
        health_prediction = model_health.predict(input_features)[0]

        irrigation_result = "Yes" if irrigation_prediction == 1 else "No"
        health_result = "Good" if health_prediction == 1 else "Poor"

        return render_template('result.html', irrigation=irrigation_result, health=health_result)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
