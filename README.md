# 🌾 Crop Infestation AI
### Predicting Crop Infestation Using Satellite Data

> **AI-powered Early Warning System for Detecting Crop Stress Before Visible Symptoms Appear**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![Google Earth Engine](https://img.shields.io/badge/Google-Earth%20Engine-green.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()

---

## 📖 Project Overview

Crop diseases and pest infestations often become visible only after significant damage has already occurred. Traditional farming methods rely on manual field inspection, which is time-consuming, expensive, and difficult to scale across large agricultural areas.

**Crop Infestation AI** is an AI-powered prototype that analyzes **Sentinel-2 multispectral satellite imagery** to detect hidden vegetation stress before symptoms become visible to the human eye.

Instead of waiting for leaves to turn yellow, the system studies how plants reflect different wavelengths of light, calculates vegetation health indices like **NDVI** and **NDRE**, extracts numerical features, and predicts an infestation risk level using a **Random Forest Machine Learning model**.

The final result is displayed through an interactive web dashboard that provides farmers with actionable recommendations.

---

# 🎯 Problem Statement

Farmers frequently discover pest attacks and crop diseases only after visible symptoms appear, leading to:

- Reduced crop yield
- Higher pesticide costs
- Delayed intervention
- Financial losses

The goal of this project is to provide an **early warning system** using satellite data and AI.

---

# 💡 Proposed Solution

Our system combines **Remote Sensing**, **Geospatial AI**, and **Machine Learning** to estimate crop infestation risk.

### User Flow

1. Select a farm location.
2. Choose a satellite acquisition date.
3. Fetch a cloud-free Sentinel-2 image.
4. Calculate vegetation health indices.
5. Generate health maps.
6. Predict infestation risk.
7. Display recommendations.

---

# 🛰️ How the System Works

## Complete Processing Pipeline

```text
Satellite Data Acquisition
        │
        ▼
Cloud Masking & Preprocessing
        │
        ▼
NDVI & NDRE Extraction
        │
        ▼
Feature Engineering
        │
        ▼
Random Forest Classification
        │
        ▼
FastAPI Prediction Service
        │
        ▼
Streamlit Dashboard
        │
        ▼
Farmer Alerts & Recommendations
```

Each module is designed independently so the project can scale into a full production system later.

---

# 🏗️ System Architecture

```text
             Google Earth Engine
                    │
        Sentinel-2 Satellite Images
                    │
                    ▼
          Cloud-Free Image Selection
                    │
                    ▼
        NDVI & NDRE Generation
                    │
                    ▼
      Feature Extraction (Numerical Data)
                    │
                    ▼
      Random Forest Machine Learning
                    │
                    ▼
         FastAPI Prediction Server
                    │
                    ▼
         Streamlit Interactive Dashboard
                    │
                    ▼
      Risk Score + Farmer Recommendation
```

---

# 🔬 Understanding the Technology

## 1. Sentinel-2 Satellite

Sentinel-2 is a European Space Agency satellite that captures Earth using multiple spectral bands.

Unlike a normal camera that only captures Red, Green, and Blue colors, Sentinel-2 also captures **Near Infrared** and **Red Edge** wavelengths, which reveal hidden plant stress.

### Why Sentinel-2?

- 10m spatial resolution
- Free and open data
- Frequent revisit time
- Multispectral bands ideal for agriculture

---

## 2. Google Earth Engine

Google Earth Engine is a cloud-based geospatial processing platform.

Instead of downloading massive satellite datasets manually, Earth Engine performs most processing on Google's servers.

We use it for:

- Satellite image retrieval
- Date filtering
- Region selection
- Cloud filtering

---

## 3. Cloud Masking

Clouds hide crops and reduce image quality.

Cloud masking removes cloudy pixels before vegetation analysis.

Think of it like removing sunglasses before taking a photograph.

---

## 4. NDVI (Normalized Difference Vegetation Index)

NDVI measures overall vegetation health.

Formula:

<math value="NDVI=\\frac{NIR-Red}{NIR+Red}" block/>

### Interpretation

| NDVI Value | Meaning |
|------------|---------|
| 0.8 | Very healthy |
| 0.5 | Moderate |
| 0.2 | Poor vegetation |
| Below 0 | Water or non-vegetation |

Plants reflect large amounts of Near Infrared light when healthy.

---

## 5. NDRE (Normalized Difference Red Edge)

NDRE detects early crop stress before visible damage appears.

Formula:

<math value="NDRE=\\frac{NIR-RedEdge}{NIR+RedEdge}" block/>

### Why NDRE Matters

- Detects nutrient deficiency
- Identifies early stress
- Useful before leaves become yellow

NDRE is one of the project's most important features.

---

## 6. Feature Engineering

After generating vegetation indices, the system extracts numerical values such as:

- Mean NDVI
- Maximum NDVI
- Minimum NDVI
- Mean NDRE

These become the input features for the Machine Learning model.

---

## 7. Machine Learning Model

We use a **Random Forest Classifier**.

### Why Random Forest?

- Beginner-friendly
- Fast training
- Handles noisy data
- Easy to explain
- Excellent baseline model

Instead of relying on a single decision tree, Random Forest combines many trees to improve prediction accuracy.

### Output Classes

- 🟢 Low Risk
- 🟡 Medium Risk
- 🔴 High Risk

---

## 8. FastAPI Backend

FastAPI connects the Machine Learning model to the dashboard.

Responsibilities:

- Load trained model
- Receive NDVI and NDRE values
- Generate predictions
- Return JSON responses

Example response:

```json
{
  "risk": "Medium",
  "score": 72
}
```

---

## 9. Streamlit Dashboard

The dashboard allows users to interact with the system.

### Dashboard Features

- Location selection
- Date selection
- Satellite image display
- NDVI heatmap
- NDRE heatmap
- Risk percentage
- Alert level
- Farmer recommendation

---

# 📂 Project Structure

```text
crop-infestation-ai/

├── assets/
│   ├── ndvi.png
│   ├── ndre.png
│   └── architecture.png
│
├── backend/
│   └── main.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   │   └── field_image.tif
│   └── processed/
│       └── features.csv
│
├── models/
│   └── model.pkl
│
├── notebooks/
│   └── training.ipynb
│
├── scripts/
│   ├── download_satellite.py
│   └── preprocessing.py
│
├── README.md
└── requirements.txt
```

---

# ⚙️ Technologies Used

## Programming

- Python 3.10+

## Geospatial Processing

- Google Earth Engine
- Sentinel-2
- Rasterio
- GDAL
- NumPy

## Machine Learning

- Scikit-learn
- Pandas
- Joblib

## Backend

- FastAPI
- Uvicorn

## Frontend

- Streamlit

## Visualization

- Matplotlib
- Geemap (Future)

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/crop-infestation-ai.git
cd crop-infestation-ai
```

## Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Start FastAPI

```bash
cd backend
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Start Streamlit

```bash
cd dashboard
streamlit run app.py
```

Dashboard opens automatically in your browser.

---

# 📊 Expected Output

The dashboard displays:

| Feature | Output |
|---------|---------|
| Satellite Image | Original Sentinel-2 |
| NDVI | Vegetation Health Map |
| NDRE | Early Stress Map |
| Risk Score | Percentage |
| Alert | Low / Medium / High |
| Recommendation | Suggested Action |

---

# 📸 Screenshots

### Dashboard

> *(Add screenshot later)*

### NDVI Map

> *(Add screenshot later)*

### NDRE Map

> *(Add screenshot later)*

### API Response

> *(Add screenshot later)*

---

# 👥 Team Responsibilities

| Member | Responsibility |
|---------|---------------|
| Member 1 | Satellite Data Acquisition |
| Member 2 | NDVI & NDRE Processing |
| Member 3 | Machine Learning |
| Member 4 | FastAPI Backend |
| Team Leader | Dashboard, Integration, GitHub |

---

# 🔄 Current Development Roadmap

## Prototype (Faculty Review)

- [x] Project planning
- [ ] Earth Engine setup
- [ ] Sentinel-2 image retrieval
- [ ] NDVI generation
- [ ] NDRE generation
- [ ] Feature extraction
- [ ] Random Forest prediction
- [ ] FastAPI backend
- [ ] Streamlit dashboard

---

## Future Enhancements

- Multi-date crop monitoring
- Weather API integration
- EVI, SAVI, GNDVI indices
- ICAR & FAO datasets
- CNN/U-Net segmentation
- Interactive field selection
- SMS & WhatsApp alerts
- Mobile application
- Real-time monitoring

---

# 🌍 Real-World Applications

This system can be used for:

- Smart Farming
- Precision Agriculture
- Government Crop Monitoring
- Agricultural Insurance
- Pest Surveillance
- Yield Optimization

---

# 📚 Key Learning Outcomes

This project demonstrates knowledge of:

- Remote Sensing
- GIS Fundamentals
- Google Earth Engine
- Multispectral Image Processing
- Vegetation Indices
- Machine Learning Classification
- FastAPI Development
- Streamlit Dashboard Development
- GitHub Collaboration Workflow

---

# 🤝 Contributing

This project follows a branch-based GitHub workflow.

Each team member works on a dedicated branch:

- `satellite-data`
- `remote-sensing`
- `machine-learning`
- `backend-api`
- `dashboard-integration`

All changes are merged into `main` through Pull Requests after review.

---

# 📄 License

This project is developed as an academic project for **VIT Bhopal University (AI & CSE Department)**.

It is intended for educational, research, and demonstration purposes.
