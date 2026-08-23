import requests
import streamlit as st
from pathlib import Path


# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000/predict"

BASE_DIR = Path(__file__).resolve().parent

RGB_IMAGE = BASE_DIR / "data" / "raw" / "rgb_preview.png"
NDVI_IMAGE = BASE_DIR / "data" / "processed" / "ndvi.png"
NDRE_IMAGE = BASE_DIR / "data" / "processed" / "ndre.png"


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Crop Infestation Detection",
    page_icon="🌾",
    layout="wide",
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🌾 Crop Infestation Detection AI")

st.markdown(
    """
    ### Sentinel-2 + NDVI + NDRE + Random Forest

    Analyze crop vegetation indices and predict potential
    crop infestation using the trained machine learning model.
    """
)

st.divider()


# --------------------------------------------------
# Input section
# --------------------------------------------------

st.subheader("🌱 Vegetation Index Input")

col1, col2 = st.columns(2)

with col1:
    ndvi = st.number_input(
        "NDVI",
        min_value=-1.0,
        max_value=1.0,
        value=0.5,
        step=0.01,
        help="Normalized Difference Vegetation Index",
    )

with col2:
    ndre = st.number_input(
        "NDRE",
        min_value=-1.0,
        max_value=1.0,
        value=0.3,
        step=0.01,
        help="Normalized Difference Red Edge Index",
    )


# --------------------------------------------------
# Prediction
# --------------------------------------------------

if st.button("🔍 Predict Crop Condition", use_container_width=True):

    payload = {
        "ndvi": ndvi,
        "ndre": ndre,
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=10,
        )

        if response.status_code == 200:

            result = response.json()

            prediction = result["prediction"]
            confidence = result["confidence"]

            st.divider()

            st.subheader("📊 Prediction Result")

            result_col1, result_col2 = st.columns(2)

            with result_col1:
                if prediction == "Healthy":
                    st.success(
                        f"🌱 Crop Condition: {prediction}"
                    )
                else:
                    st.warning(
                        f"⚠️ Crop Condition: {prediction}"
                    )

            with result_col2:
                st.metric(
                    "Model Confidence",
                    f"{confidence:.2f}%"
                )

        else:

            st.error(
                f"API returned error {response.status_code}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the FastAPI backend. "
            "Make sure Uvicorn is running on port 8000."
        )

    except requests.exceptions.Timeout:

        st.error(
            "❌ The prediction request timed out."
        )

    except Exception as e:

        st.error(
            f"❌ Unexpected error: {str(e)}"
        )


# --------------------------------------------------
# Satellite imagery
# --------------------------------------------------

st.divider()

st.subheader("🛰️ Satellite Analysis")

image_col1, image_col2, image_col3 = st.columns(3)


with image_col1:

    st.markdown("### RGB Preview")

    if RGB_IMAGE.exists():
        st.image(
            str(RGB_IMAGE),
            use_container_width=True,
        )
    else:
        st.warning("RGB image not found.")


with image_col2:

    st.markdown("### NDVI")

    if NDVI_IMAGE.exists():
        st.image(
            str(NDVI_IMAGE),
            use_container_width=True,
        )
    else:
        st.warning("NDVI image not found.")


with image_col3:

    st.markdown("### NDRE")

    if NDRE_IMAGE.exists():
        st.image(
            str(NDRE_IMAGE),
            use_container_width=True,
        )
    else:
        st.warning("NDRE image not found.")


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Crop Infestation Detection AI • "
    "Sentinel-2 • NDVI • NDRE • Random Forest • FastAPI • Streamlit"
)