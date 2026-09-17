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
    page_title="Crop Infestation Detection AI",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">

<style>

:root{
    --green-900:#1B4D2E;
    --green-700:#2E7D32;
    --green-600:#37934A;
    --green-100:#E8F5E9;
    --ink:#111418;
    --muted:#5B6672;
    --border:#E5E7EB;
    --card-bg:#FFFFFF;
    --page-bg:#F6F8F7;
}

html, body, [class*="css"]{
    font-family:'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp{
    background:var(--page-bg);
}

/* Full width layout, edge to edge */
.block-container{
    max-width:100% !important;
    padding-top:1.4rem;
    padding-bottom:3rem;
    padding-left:2.4rem;
    padding-right:2.4rem;
}

header,#MainMenu,footer{
    visibility:hidden;
}

/* ---------- Hero ---------- */

.hero-wrap{
    background:linear-gradient(135deg, var(--green-900) 0%, var(--green-600) 100%);
    border-radius:18px;
    padding:2.4rem 2.6rem;
    margin-bottom:1.8rem;
    box-shadow:0 10px 30px rgba(27,77,46,0.16);
}

.hero-eyebrow{
    display:inline-block;
    background:rgba(255,255,255,0.15);
    color:#EAF7EC;
    font-size:0.76rem;
    font-weight:600;
    letter-spacing:1.2px;
    text-transform:uppercase;
    padding:6px 14px;
    border-radius:999px;
    margin-bottom:14px;
}

.hero-title{
    font-family:'Poppins', 'Inter', sans-serif;
    color:#FFFFFF !important;
    font-size:2.5rem !important;
    font-weight:800 !important;
    letter-spacing:-0.5px;
    margin:0 0 10px 0 !important;
    line-height:1.15;
}

.hero-subtitle{
    color:rgba(255,255,255,0.88) !important;
    font-size:1.03rem !important;
    line-height:1.65;
    max-width:800px;
    margin:0 !important;
}

.hero-tags{
    margin-top:18px;
    display:flex;
    flex-wrap:wrap;
    gap:8px;
}

.hero-tag{
    background:rgba(255,255,255,0.14);
    border:1px solid rgba(255,255,255,0.25);
    color:#FFFFFF;
    font-size:0.8rem;
    font-weight:500;
    padding:5px 12px;
    border-radius:8px;
}

/* ---------- Section headings ---------- */

.section-title{
    font-family:'Poppins','Inter',sans-serif;
    color:var(--ink) !important;
    font-size:1.3rem !important;
    font-weight:700 !important;
    margin-bottom:2px !important;
}

.section-subtitle{
    color:var(--muted) !important;
    font-size:0.92rem !important;
    margin-bottom:1rem !important;
}

p, li{
    color:#333333;
    font-size:1.02rem;
    line-height:1.7;
}

/* ---------- Cards (native st.container(border=True)) ---------- */

div[data-testid="stVerticalBlockBorderWrapper"]{
    background:var(--card-bg);
    border:1px solid var(--border) !important;
    border-radius:16px !important;
    box-shadow:0 2px 10px rgba(16,24,40,0.04);
}

div[data-testid="stVerticalBlockBorderWrapper"] > div{
    border-radius:16px;
}

/* ---------- Metrics ---------- */

[data-testid="stMetric"]{
    background:var(--green-100);
    border-radius:12px;
    padding:14px 16px;
}

[data-testid="stMetricLabel"]{
    color:var(--muted) !important;
    font-weight:600;
    font-size:0.85rem !important;
    text-transform:uppercase;
    letter-spacing:0.4px;
}

[data-testid="stMetricValue"]{
    color:var(--green-900) !important;
    font-size:1.9rem !important;
    font-weight:800 !important;
}

/* ---------- Inputs: keep them compact, not full-width bars ---------- */

[data-testid="stNumberInput"]{
    max-width:220px;
}

[data-testid="stNumberInput"] label{
    font-weight:600 !important;
    color:var(--ink) !important;
    font-size:0.95rem !important;
}

[data-testid="stNumberInput"] input{
    border-radius:10px !important;
    font-weight:600;
}

/* ---------- Buttons ---------- */

.stButton>button{
    width:auto;
    min-width:240px;
    background:var(--green-700);
    color:white;
    border:none;
    border-radius:12px;
    padding:12px 28px;
    font-size:16px;
    font-weight:700;
    letter-spacing:0.2px;
    transition:all 0.15s ease-in-out;
    box-shadow:0 4px 14px rgba(46,125,50,0.28);
}

.stButton>button:hover{
    background:var(--green-900);
    box-shadow:0 6px 18px rgba(27,77,46,0.32);
    transform:translateY(-1px);
}

/* ---------- Images ---------- */

[data-testid="stImage"] img{
    border-radius:14px;
    border:1px solid var(--border);
    height:280px;
    width:100%;
    object-fit:cover;
}

.image-title{
    font-size:1.02rem;
    font-weight:700;
    color:var(--ink);
    margin-bottom:10px;
}

/* ---------- Progress bar ---------- */

[data-testid="stProgress"] > div > div{
    background:var(--green-700) !important;
}

/* ---------- Footer ---------- */

.footer{
    text-align:center;
    color:#8A8F98;
    font-size:13.5px;
    padding-top:8px;
    letter-spacing:0.2px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Hero
# --------------------------------------------------

st.markdown("""
<div class="hero-wrap">
    <span class="hero-eyebrow">Remote Sensing &nbsp;&bull;&nbsp; AI Early-Warning System</span>
    <h1 class="hero-title">Crop Infestation Detection AI</h1>
    <p class="hero-subtitle">
        Early warning system that analyzes vegetation indices from satellite imagery
        and predicts potential crop infestation before visible symptoms become severe.
    </p>
    <div class="hero-tags">
        <span class="hero-tag">Sentinel-2</span>
        <span class="hero-tag">NDVI</span>
        <span class="hero-tag">NDRE</span>
        <span class="hero-tag">Random Forest</span>
        <span class="hero-tag">FastAPI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Dashboard Cards
# --------------------------------------------------

st.markdown('<div class="section-title">Field Snapshot</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Live vegetation health indicators for the selected field</div>', unsafe_allow_html=True)

with st.container(border=True):
    m1, m2, m3 = st.columns(3)

    with m1:
        ndvi_metric = st.empty()

    with m2:
        ndre_metric = st.empty()

    with m3:
        st.metric("Cloud Cover", "0.0%")

# --------------------------------------------------
# Input Section
# --------------------------------------------------

st.markdown('<div class="section-title" style="margin-top:1.8rem;">Vegetation Index Input</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Adjust values manually or feed them from the processing pipeline</div>', unsafe_allow_html=True)

with st.container(border=True):
    col1, col2, col_spacer = st.columns([1, 1, 3])

    with col1:
        ndvi = st.number_input(
            "NDVI",
            min_value=-1.0,
            max_value=1.0,
            value=0.50,
            step=0.01,
            help="Normalized Difference Vegetation Index"
        )

    with col2:
        ndre = st.number_input(
            "NDRE",
            min_value=-1.0,
            max_value=1.0,
            value=0.30,
            step=0.01,
            help="Normalized Difference Red Edge Index"
        )

    # Update metric cards
    ndvi_metric.metric("NDVI", f"{ndvi:.2f}")
    ndre_metric.metric("NDRE", f"{ndre:.2f}")

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    predict_clicked = st.button("Predict Crop Condition")

# --------------------------------------------------
# Prediction
# --------------------------------------------------

if predict_clicked:

    payload = {
        "ndvi": ndvi,
        "ndre": ndre
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:

            result = response.json()

            prediction = result["prediction"]
            confidence = result["confidence"]
            risk = int(round(result["infestation_risk"]))

            st.markdown('<div class="section-title" style="margin-top:1.8rem;">Prediction Dashboard</div>', unsafe_allow_html=True)

            with st.container(border=True):

                left, right = st.columns([3, 1])

                with left:

                    if prediction == "Healthy":
                        st.success(f"Crop Condition: {prediction}")
                    else:
                        st.error(f"Crop Condition: {prediction}")

                with right:

                    st.metric("Model Confidence", f"{confidence:.2f}%")

                st.markdown("### Infestation Risk")

                st.progress(risk)

                st.metric("Risk Level", f"{risk}%")

                st.markdown("### Recommended Action")

                if prediction == "Healthy":
                    st.success(
                        "Crop appears healthy. Continue routine monitoring and maintain irrigation and nutrient schedules."
                    )
                else:
                    st.error(
                        "High infestation risk detected. Inspect the field within 24–48 hours and consider early intervention."
                    )

        else:
            st.error(f"API returned error {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to the FastAPI backend. Make sure Uvicorn is running on port 8000."
        )

    except requests.exceptions.Timeout:
        st.error("Prediction request timed out.")

    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")

# --------------------------------------------------
# Satellite Analysis
# --------------------------------------------------

st.markdown('<div class="section-title" style="margin-top:2rem;">Satellite Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Visual comparison of raw imagery and derived vegetation indices</div>', unsafe_allow_html=True)

img1, img2, img3 = st.columns(3)

with img1:

    with st.container(border=True):

        st.markdown(
            '<div class="image-title">RGB Preview</div>',
            unsafe_allow_html=True
        )

        if RGB_IMAGE.exists():
            st.image(str(RGB_IMAGE), use_container_width=True)
        else:
            st.warning("RGB image not found.")

with img2:

    with st.container(border=True):

        st.markdown(
            '<div class="image-title">NDVI Map</div>',
            unsafe_allow_html=True
        )

        if NDVI_IMAGE.exists():
            st.image(str(NDVI_IMAGE), use_container_width=True)
        else:
            st.warning("NDVI image not found.")

with img3:

    with st.container(border=True):

        st.markdown(
            '<div class="image-title">NDRE Map</div>',
            unsafe_allow_html=True
        )

        if NDRE_IMAGE.exists():
            st.image(str(NDRE_IMAGE), use_container_width=True)
        else:
            st.warning("NDRE image not found.")

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer">
    Crop Infestation Detection AI &bull; Sentinel-2 &bull; NDVI &bull; NDRE &bull; Random Forest &bull; FastAPI &bull; Streamlit
    </div>
    """,
    unsafe_allow_html=True
)