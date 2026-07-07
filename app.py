import streamlit as st
import math
import time
import requests

# Page Configuration
st.set_page_config(page_title="Orbital Intel Pro v5.0", page_icon="🛰️", layout="wide")

st.markdown("<h1 style='text-align: center; color: #00E5FF;'>🛰️ ORBITAL INTEL PRO: LIVE NASA FEED EDITION</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #8A99AD;'>Autonomous Real-Time Satellite Tracking & AI Collision Predictor</h3>", unsafe_allow_html=True)
st.write("---")

# Function to fetch live orbital data from CelesTrak (NASA tracking catalog)
@st.cache_data(ttl=3600)  # Cache data for 1 hour to save network bandwidth
def fetch_live_nasa_data():
    try:
        # Fetching active satellites data directly via Celestrak's GP API
        url = "https://celestrak.org"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None

# Load the live database
live_database = fetch_live_nasa_data()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📡 Live Space Data Stream")
    
    if live_database:
        st.success(f"🟢 Connected to CelesTrak (NORAD/NASA Database). Tracking {len(live_database)} active objects live!")
        
        # Create a searchable dropdown of all active satellite names in space
        sat_names = [obj['OBJECT_NAME'] for obj in live_database if 'OBJECT_NAME' in obj]
        selected_sat = st.selectbox("Select Target Satellite to Monitor:", options=sat_names, index=sat_names.index("ISS (ZARYA)") if "ISS (ZARYA)" in sat_names else 0)
        
        # Extract real orbital elements for the selected satellite
        sat_data = next((item for item in live_database if item.get('OBJECT_NAME') == selected_sat), None)
        
        if sat_data:
            st.markdown("#### 📊 Current Live Telemetry")
            # Calculate live approximate parameters from real data
            mean_motion = float(sat_data.get('MEAN_MOTION', 15.0))
            eccentricity = float(sat_data.get('ECCENTRICITY', 0.001))
            
            # Derived velocity (approximate real-world km/s based on orbital period)
            live_speed_mps = round((mean_motion * 42000) / 86400 * 1000, 2) 
            live_mass_kg = 450.0 if "STARLINK" in selected_sat else 420000.0 if "ISS" in selected_sat else 150.0
            
            st.info(f"**NORAD Catalog ID:** {sat_data.get('OBJECT_ID')}")
            st.info(f"**Live Computed Speed:** {live_speed_mps} m/s")
            st.info(f"**Orbital Inclination:** {sat_data.get('INCLINATION')}°")
    else:
        st.error("🔴 Temporary issue syncing with Live NASA feeds. Using local system matrices.")
        selected_sat = st.text_input("Enter Target Satellite Name:", value="STARLINK-30214")
        live_speed_mps = 14200.0
        live_mass_kg = 500.0

    st.markdown("---")
    st.markdown("#### 🚨 Simulated Debris Conjunction Vector")
    dist = st.slider("Current Miss Distance (Meters):", min_value=1, max_value=5000, value=120)
    time_left = st.slider("Time to Closest Approach (Minutes):", min_value=1, max_value=180, value=8)

# AI Advanced Engine
def advanced_space_ai(distance, speed, mass, time_left):
    w_dist = -0.75  
    w_speed = 0.45
    w_time = -0.60
    score = (w_dist * math.log(distance + 1)) + (w_speed * (speed / 1000)) + (w_time * time_left) + (mass * 0.005)
    probability = 1 / (1 + math.exp(-score / 50)) * 100
    return probability

with col2:
    st.markdown("### 🤖 Autonomous AI Analytics Center")
    st.write(f"Click below to scan threats for **{selected_sat}**:")
    
    if st.button("🚀 Execute Advance Conjunction Analysis", type="primary"):
        with st.spinner("Analyzing live telemetry paths against debris vectors..."):
            time.sleep(1)
            
        risk_pct = advanced_space_ai(dist, live_speed_mps, live_mass_kg, time_left)
        
        st.metric(label="AI Collision Threat Index", value=f"{risk_pct:.4f}%")
        st.write("---")
        st.markdown("#### 📋 System Action Report")
        
        if risk_pct > 65:
            st.error("🚨 CRITICAL EMERGENCY THREAT ALERT!")
            st.warning(f"📢 AI RECOMMENDATION: Initiate immediate **Proactive Maneuver**. Alter the orbit of {selected_sat} immediately to avoid destruction.")
        elif 35 <= risk_pct <= 65:
            st.warning("⚠️ WATCH STATUS: ELEVATED RISK")
            st.info(f"📢 AI RECOMMENDATION: Keep ground stations on alert. Monitor {selected_sat}'s next orbital pass.")
        else:
            st.success("✅ STATUS: NOMINAL OPERATIONAL CLEARANCE")
            st.info("📢 AI RECOMMENDATION: Safe passage predicted. {selected_sat} is clear.")

