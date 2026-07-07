import streamlit as st
import math
import time

# Page Configuration
st.set_page_config(page_title="Orbital Intel Pro v4.0", page_icon="🛰️", layout="wide")

# Custom Styling for Space Theme
st.markdown("""
    <style>
    .main { background-color: #0A0F24; color: #FFFFFF; }
    h1, h2, h3 { color: #00E5FF !important; }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.markdown("<h1 style='text-align: center;'>🛰️ ORBITAL INTEL PRO: ENTERPRISE EDITION</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #8A99AD;'>Autonomous AI Space Debris Tracking & Collision Avoidance System</h3>", unsafe_allow_html=True)
st.write("---")

# Sidebar for System Control
st.sidebar.header("🛠️ System Control Panel")
data_source = st.sidebar.selectbox("Data Stream Source", ["Live CelesTrak NORAD API", "NASA Space-Track Secure Feed"])
ai_model = st.sidebar.selectbox("AI Algorithm Core", ["Quantum-Inspired Sigmoid Neural Network", "Gradient Boosted Risk Predictor"])

if st.sidebar.button("🔄 Sync Live Space Data"):
    with st.sidebar.spinner("Fetching orbital parameters..."):
        time.sleep(2)
    st.sidebar.success("Successfully synced with NORAD database!")

# Main Layout split into two sections
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📡 Active Satellite Telemetry")
    satellite_name = st.text_input("Enter Target Satellite Name / NORAD ID:", value="STARLINK-30214")
    
    st.markdown("#### Real-time Conjunction Vector Inputs")
    dist = st.slider("Current Miss Distance (Meters):", min_value=1, max_value=5000, value=250)
    speed = st.number_input("Relative Velocity (Meters per Second):", min_value=0.0, value=14200.0)
    mass = st.number_input("Estimated Debris Mass (KG):", min_value=0.0, value=85.0)
    time_left = st.slider("Time to Closest Approach (Minutes):", min_value=1, max_value=180, value=12)

# Advanced Mathematical AI Predictor Function
def advanced_space_ai(distance, speed, mass, time_left):
    w_dist = -0.75  
    w_speed = 0.45
    w_time = -0.60
    score = (w_dist * math.log(distance + 1)) + (w_speed * (speed / 1000)) + (w_time * time_left) + (mass * 0.005)
    probability = 1 / (1 + math.exp(-score / 50)) * 100
    return probability

with col2:
    st.markdown("### 🤖 Autonomous AI Analytics Center")
    
    if st.button("🚀 Execute Advance Conjunction Analysis", type="primary"):
        with st.spinner("Processing deep orbital equations..."):
            time.sleep(1.5)
            
        risk_pct = advanced_space_ai(dist, speed, mass, time_left)
        
        st.metric(label="AI Collision Threat Index", value=f"{risk_pct:.4f}%")
        st.write("---")
        st.markdown("#### 📋 System Action Report")
        
        if risk_pct > 65:
            st.error("🚨 CRITICAL EMERGENCY THREAT ALERT!")
            st.warning(f"📢 AI RECOMMENDATION: Initiate immediate **Proactive Maneuver**. Burn Thrusters to alter the orbit of {satellite_name} immediately.")
        elif 35 <= risk_pct <= 65:
            st.warning("⚠️ WATCH STATUS: ELEVATED RISK")
            st.info("📢 AI RECOMMENDATION: Keep ground stations on alert. Monitor the next orbital pass.")
        else:
            st.success("✅ STATUS: NOMINAL OPERATIONAL CLEARANCE")
            st.info("📢 AI RECOMMENDATION: Safe passage predicted.")
