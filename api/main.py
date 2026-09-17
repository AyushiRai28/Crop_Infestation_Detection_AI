from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import numpy as np

# --------------------------------------------------
# Load Trained Model
# --------------------------------------------------
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "random_forest.joblib"

model = joblib.load(MODEL_PATH)

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="Crop Infestation Detection API",
    description="AI-powered crop infestation detection using NDVI and NDRE",
    version="1.0.0"
)

# --------------------------------------------------
# Input Schema
# --------------------------------------------------

class CropInput(BaseModel):
    ndvi: float = Field(..., ge=-1.0, le=1.0)
    ndre: float = Field(..., ge=-1.0, le=1.0)

# --------------------------------------------------
# Home Route
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Crop Infestation Detection API is running"
    }

# --------------------------------------------------
# Prediction Route
# --------------------------------------------------

@app.post("/predict")
def predict(data: CropInput):

    features = np.array([[data.ndvi, data.ndre]])

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    healthy_prob = float(probabilities[0]) * 100
    infested_prob = float(probabilities[1]) * 100

    return {
        "prediction": "Potentially Infested" if int(prediction) else "Healthy",
        "class": int(prediction),
        "confidence": round(max(healthy_prob, infested_prob), 2),
        "infestation_risk": round(infested_prob, 2)
    }
