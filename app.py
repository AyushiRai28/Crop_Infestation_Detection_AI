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
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Crop Infestation Detection",      # Change browser tab name here
    page_icon=" ",
    layout="wide" ,
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

/* ---------- Page ---------- */

.stApp{
    background:#ffffff;
}

.block-container{
    max-width:96%;
    padding-top:1.2rem;
    padding-bottom:2rem;
}

header,
#MainMenu,
footer{
    visibility:hidden;
}

/* ---------- Main Title (st.title) ---------- */

[data-testid="stHeading"] h1{
    color:#111111 !important;
    font-size:4.8rem !important;
    font-weight:800 !important;
    letter-spacing:-2px;
    line-height:1.05;
    margin-bottom:0.8rem;
}

/* ---------- Section Titles ---------- */

[data-testid="stHeading"] h2{
    color:#111111 !important;
    font-size:2.5rem !important;
    font-weight:700 !important;
    letter-spacing:-0.8px;
    margin-top:2rem;
    margin-bottom:1rem;
}

[data-testid="stHeading"] h3{
    color:#111111 !important;
    font-size:1.8rem !important;
    font-weight:600 !important;
    margin-bottom:0.8rem;
}

/* ---------- Body Text ---------- */

p, li{
    color:#333333 !important;
    font-size:1.15rem !important;
    line-height:1.7;
}

/* ---------- Labels ---------- */

.stNumberInput label{
    color:#111111 !important;
    font-weight:600 !important;
    font-size:1rem !important;
}

/* ---------- Number Inputs ---------- */

.stNumberInput input{
    background:white !important;
    color:#111111 !important;
    border:1px solid #d4d4d4 !important;
    border-radius:10px !important;
}

/* ---------- Button ---------- */

.stButton > button{
    width:100%;
    background:#2E7D32;
    color:white;
    border:none;
    border-radius:10px;
    padding:14px;
    font-size:17px;
    font-weight:600;
}

.stButton > button:hover{
    background:#276C2A;
}

/* ---------- Metric ---------- */

[data-testid="stMetricLabel"]{
    color:#111111 !important;
    font-weight:600;
    font-size:1rem !important;
}

[data-testid="stMetricValue"]{
    color:#111111 !important;
    font-size:2.2rem !important;
    font-weight:700;
}

/* ---------- Image Titles ---------- */

.image-title{
    color:#111111;
    font-size:1.25rem;
    font-weight:600;
    margin-bottom:10px;
}

/* ---------- Images ---------- */

[data-testid="stImage"] img{
    border-radius:12px;
    border:1px solid #E5E7EB;
}

/* ---------- Footer ---------- */

.footer{
    text-align:center;
    color:#7A7A7A;
    font-size:14px;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Hero
# --------------------------------------------------

st.title("Crop Infestation Detection AI")

st.markdown("""
**Sentinel-2 • NDVI • NDRE • Random Forest**

Analyze crop vegetation indices and predict potential crop infestation using the trained machine learning model.
""")

st.divider()

# --------------------------------------------------
# Input Section
# --------------------------------------------------

st.subheader("Vegetation Index Input")

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

if st.button("🔍 Predict Crop Condition"):

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

            st.subheader("Prediction Result")

            left, right = st.columns([3,1])

            with left:

                if prediction == "Healthy":
                    st.success(f"Crop Condition: {prediction}")
                else:
                    st.warning(f"⚠️ Crop Condition: {prediction}")

            with right:

                st.metric(
                    "Confidence",
                    f"{confidence:.2f}%"
                )

        else:

            st.error(
                f"API returned error {response.status_code}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the FastAPI backend. Make sure Uvicorn is running on port 8000."
        )

    except requests.exceptions.Timeout:

        st.error(
            "❌ Prediction request timed out."
        )

    except Exception as e:

        st.error(
            f"❌ Unexpected error: {str(e)}"
        )

# --------------------------------------------------
# Satellite Analysis
# --------------------------------------------------

st.divider()

st.subheader("Satellite Analysis")

image_col1, image_col2, image_col3 = st.columns(3)

with image_col1:

    st.markdown(
        '<div class="image-title">RGB Preview</div>',
        unsafe_allow_html=True,
    )

    if RGB_IMAGE.exists():
        st.image(
            str(RGB_IMAGE),
            use_container_width=True,
        )
    else:
        st.warning("RGB image not found.")

with image_col2:

    st.markdown(
        '<div class="image-title">NDVI</div>',
        unsafe_allow_html=True,
    )

    if NDVI_IMAGE.exists():
        st.image(
            str(NDVI_IMAGE),
            use_container_width=True,
        )
    else:
        st.warning("NDVI image not found.")

with image_col3:

    st.markdown(
        '<div class="image-title">NDRE</div>',
        unsafe_allow_html=True,
    )

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

st.markdown(
    """
    <div class="footer">
    Crop Infestation Detection AI • Sentinel-2 • NDVI • NDRE • Random Forest • FastAPI • Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)