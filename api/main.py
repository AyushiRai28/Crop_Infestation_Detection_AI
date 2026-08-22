from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import numpy as np

# Load trained model
model = joblib.load("models/random_forest.joblib")

app = FastAPI(
    title="Crop Infestation Detection API",
    description="AI-powered crop infestation detection using NDVI and NDRE",
    version="1.0.0"
)


# Request format
class CropInput(BaseModel):
    ndvi: float = Field(..., ge=-1.0, le=1.0)
    ndre: float = Field(..., ge=-1.0, le=1.0)


@app.get("/")
def home():
    return {
        "message": "Crop Infestation Detection API is running"
    }


@app.post("/predict")
def predict(data: CropInput):

    # Prepare features in the same order used during training
    features = np.array([[data.ndvi, data.ndre]])

    # Get prediction
    prediction = model.predict(features)[0]

    # Get probabilities
    probabilities = model.predict_proba(features)[0]

    # Find probability corresponding to predicted class
    prediction_index = list(model.classes_).index(prediction)

    probability = float(probabilities[prediction_index])

    return {
        "prediction": "Potentially Infested" if int(prediction) else "Healthy",
        "class": int(prediction),
        "confidence": round(probability * 100, 2)
    }

