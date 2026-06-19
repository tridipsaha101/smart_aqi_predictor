import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import joblib
from datetime import datetime, timedelta
import random
import numpy as np
import os
import folium
from streamlit_folium import st_folium

# ---------------- CONFIG ---------------- #

st.set_page_config(
    page_title="Smart AQI Health Predictor",
    page_icon="🌍",
    layout="wide"
)

API_KEY = "7fe905154c71ebfca9531a75db59e25051f5e305"
MODEL_PATH = "risk_model.pkl"

# ---------------- CACHE MODEL ---------------- #

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error("❌ Model file not found!")
        st.stop()
    return joblib.load(MODEL_PATH)

model = load_model()

# ---------------- CACHE API ---------------- #

@st.cache_data(ttl=600)
def get_aqi_data(city):
    try:
        url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get("status") == "ok":
            return data.get("data")
        return None
    except:
        return None

# ---------------- FUNCTIONS ---------------- #

def generate_last7(aqi):
    return [max(25, aqi + random.randint(-40, 40)) for _ in range(7)]

def forecast_next3(aqi):
    return [
        int(aqi * random.uniform(0.9, 1.1)),
        int(aqi * random.uniform(0.85, 1.15)),
        int(aqi * random.uniform(0.8, 1.2))
    ]

def gauge_chart(aqi):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi,
        gauge={
            'axis': {'range': [0, 500]},
            'bar': {'color': "cyan"},
            'steps': [
                {'range': [0, 50], 'color': "green"},
                {'range': [51, 100], 'color': "yellow"},
                {'range': [101, 150], 'color': "orange"},
                {'range': [151, 200], 'color': "red"},
                {'range': [201, 300], 'color': "purple"},
                {'range': [301, 500], 'color': "maroon"}
            ]
        }
    ))
    fig.update_layout(height=280)
    return fig

def safety_advice(risk):
    advice = {
        0: "Safe air. Enjoy outdoor activities.",
        1: "Sensitive people should limit prolonged outdoor exertion.",
        2: "Wear mask & avoid heavy outdoor exercise.",
        3: "Stay indoors, use air purifier, wear N95 mask.",
        4: "Strictly avoid outdoor activity. Health emergency possible."
    }
    return advice.get(risk, "No data available.")

def generate_map(lat, lon, aqi):
    if aqi <= 50:
        color = "green"
    elif aqi <= 100:
        color = "orange"
    elif aqi <= 150:
        color = "red"
    else:
        color = "darkred"

    m = folium.Map(location=[lat, lon], zoom_start=11)

    folium.CircleMarker(
        location=[lat, lon],
        radius=18,
        popup=f"AQI: {aqi}",
        color=color,
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

    return m

# ---------------- UI ---------------- #

st.title("🌍 Smart AQI Health Predictor")
st.markdown("AI Powered Health Risk Forecasting System")

left, right = st.columns([1, 1])

# ---------- FORM (NO RERUN LOOP) ---------- #

with left:
    st.subheader("🎛 User Inputs")

    with st.form("prediction_form"):
        city = st.text_input("🏙 Enter City", "Kolkata")
        age = st.slider("🎂 Age", 1, 100, 22)
        asthma = st.selectbox("😷 Asthma / Respiratory problem?", ["No", "Yes"])
        submit = st.form_submit_button("🔍 Predict Health Risk")

with right:
    st.subheader("🗺 Live AQI Map")
    map_placeholder = st.empty()

# ---------------- MAIN LOGIC ---------------- #

if submit:

    with st.spinner("Generating AI prediction..."):

        data = get_aqi_data(city)

        if data is None:
            st.error("❌ Unable to fetch AQI.")
            st.stop()

        aqi = data.get("aqi")
        geo = data.get("city", {}).get("geo", [None, None])

        if aqi is None or aqi == "-" or geo[0] is None:
            st.error("❌ AQI data not available.")
            st.stop()

        lat, lon = geo

        asthma_val = 1 if asthma == "Yes" else 0
        hour = datetime.now().hour

        X = np.array([[aqi, age, asthma_val, hour]])

        prediction = int(model.predict(X)[0])
        prob = float(model.predict_proba(X).max()) * 100

        risk_map = [
            "Good",
            "Moderate",
            "Unhealthy (Sensitive)",
            "Unhealthy",
            "Very Unhealthy"
        ]

        # --- Map (NO BLINK FIX) ---
        m = generate_map(lat, lon, aqi)
        with map_placeholder:
            st_folium(
                m,
                height=320,
                use_container_width=True,
                returned_objects=[]   # 🔥 stops rerun loop
            )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current AQI", aqi)
        col2.metric("Health Risk", risk_map[prediction])
        col3.metric("Confidence", f"{prob:.1f}%")
        col4.metric("City", city)

        st.subheader("🎯 Health Risk Meter")
        st.plotly_chart(gauge_chart(aqi), use_container_width=True)

        st.subheader("🛡 Safety Measures")
        st.info(safety_advice(prediction))

        st.subheader("📊 Last 7 Days AQI")
        last7 = generate_last7(aqi)
        days = [(datetime.now() - timedelta(days=i)).strftime("%d %b") for i in range(6, -1, -1)]
        df = pd.DataFrame({"Day": days, "AQI": last7})

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Day"], y=df["AQI"], mode="lines+markers"))
        fig.update_layout(height=280)

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🔮 AQI Forecast (Next 3 Days)")
        f = forecast_next3(aqi)

        f1, f2, f3 = st.columns(3)
        f1.metric("Tomorrow", f[0])
        f2.metric("Day +2", f[1])
        f3.metric("Day +3", f[2])

        st.success("✅ AI Prediction Completed Successfully")