from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load trained model
model = joblib.load("models/random_forest.joblib")

app = FastAPI(title="Crop Infestation Detection API")

# Request format
class CropInput(BaseModel):
    ndvi: float
    ndre: float

@app.get("/")
def home():
    return {
        "message": "Crop Infestation Detection API is running"
    }

@app.post("/predict")
def predict(data: CropInput):

    features = np.array([[data.ndvi, data.ndre]])

    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][prediction])

    return {
        "prediction": "Potentially Infested" if prediction else "Healthy",
        "class": prediction,
        "confidence": round(probability * 100, 2)
    }


