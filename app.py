import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- SYSTEM CONFIGURATION ---
st.set_page_config(page_title="MotoIntel AI | PrAv", layout="wide", page_icon="🏍️")

# --- INDUSTRIAL UI STYLING (REFINED) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');
    
    .stApp { background-color: #050505; color: #00d4ff; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00d4ff; text-align: center; font-size: 2.5rem; letter-spacing: 8px; margin-bottom: 0px; }
    .sub-header { font-family: 'JetBrains Mono', monospace; color: #444; text-align: center; font-size: 0.7rem; letter-spacing: 4px; margin-bottom: 40px; }
    .metric-card { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 20px; text-align: center; }
    
    /* Remove streamlit branding for premium look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- DIAGNOSTIC ENGINE ---
def run_evaluation(temp, rpm, vib, bat):
    health = 100
    logs = []
    
    if temp > 105:
        health -= 40
        logs.append("CRITICAL: THERMAL EXCURSION")
    elif temp > 95:
        health -= 15
        logs.append("CAUTION: ELEVATED TEMPERATURE")
        
    if vib > 0.7 and rpm < 4000:
        health -= 30
        logs.append("ANOMALY: MECHANICAL VIBRATION")
        
    if bat < 11.8:
        health -= 20
        logs.append("ELECTRICAL: VOLTAGE DEGRADATION")
    
    return max(health, 0), logs

# --- INTERFACE ---
st.markdown('<p class="main-header">MOTOINTEL AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">PROJECT ARCHITECTURE BY PRAV</p>', unsafe_allow_html=True)

# Sensor Data via Sidebar (For Manual Testing/Wokwi Simulation)
with st.sidebar:
    st.markdown("### 📡 TELEMETRY NODE")
    in_temp = st.slider("Engine Temp (°C)", 40, 150, 90)
    in_rpm = st.slider("Crankshaft RPM", 0, 14000, 4500)
    in_vib = st.slider("Vibration Index", 0.0, 1.0, 0.15)
    in_bat = st.slider("Battery Voltage", 10.0, 14.5, 12.6)

health_val, alerts = run_evaluation(in_temp, in_rpm, in_vib, in_bat)

# Main Dashboard Layout
c1, c2, c3 = st.columns([1, 2, 1])

with c1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("THERMAL", f"{in_temp}°C")
    st.metric("RPM", f"{in_rpm}")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = health_val,
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "#444"},
            'bar': {'color': "#00d4ff" if health_val > 70 else "#ffaa00" if health_val > 40 else "#ff1111"},
            'bgcolor': "#0a0a0a",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(255, 0, 0, 0.05)'},
                {'range': [70, 100], 'color': 'rgba(0, 212, 255, 0.05)'}],
            'borderwidth': 1,
            'bordercolor': "#222"
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        font={'color': "#00d4ff", 'family': "Orbitron"}, 
        margin=dict(t=0, b=0, l=10, r=10)
    )
    
    # FIXED: Using width="stretch" to eliminate 2026 warnings
    st.plotly_chart(fig, width="stretch")

with c3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("SEISMIC", f"{in_vib}G")
    st.metric("VOLTAGE", f"{in_bat}V")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Diagnostic Logs
st.subheader("DIAGNOSTIC LOG ANALYSIS")
if not alerts:
    st.info("NO ANOMALIES DETECTED. SYSTEM NOMINAL.")
else:
    for a in alerts:
        st.error(a)

st.markdown(f"<p style='text-align: right; color: #222; font-size: 10px; letter-spacing: 2px;'>NODE_SECURE | {datetime.now().strftime('%Y-%m-%d')} | PR AV</p>", unsafe_allow_html=True)
