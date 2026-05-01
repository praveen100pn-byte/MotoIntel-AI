import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- SYSTEM ARCHITECTURE CONFIG ---
st.set_page_config(page_title="MotoIntel AI | PrAv", layout="wide")

# --- INDUSTRIAL UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');
    
    .stApp { background-color: #050505; color: #00d4ff; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00d4ff; text-align: center; font-size: 3rem; letter-spacing: 8px; margin-bottom: 0px; }
    .sub-header { font-family: 'JetBrains Mono', monospace; color: #444; text-align: center; font-size: 0.75rem; letter-spacing: 4px; margin-bottom: 50px; }
    .metric-container { background: #0d0d0d; border: 1px solid #1a1a1a; border-radius: 4px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DIAGNOSTIC PROCESSING ---
def evaluate_telemetry(temp, rpm, vib, bat):
    health = 100
    logs = []
    
    if temp > 105:
        health -= 40
        logs.append("CRITICAL: THERMAL EXCURSION DETECTED")
    elif temp > 95:
        health -= 15
        logs.append("CAUTION: OPERATING ABOVE NOMINAL TEMPERATURE")
        
    if vib > 0.7 and rpm < 4000:
        health -= 30
        logs.append("ANOMALY: LOW-FREQUENCY MECHANICAL VIBRATION")
        
    if bat < 11.8:
        health -= 20
        logs.append("ELECTRICAL: VOLTAGE NODE DEGRADATION")
    
    return max(health, 0), logs

# --- INTERFACE ---
st.markdown('<p class="main-header">MOTOINTEL AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">SYSTEM DESIGN BY PRAV</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### HARDWARE INTERFACE")
    in_temp = st.slider("Engine Temp (°C)", 40, 150, 90)
    in_rpm = st.slider("Crankshaft RPM", 0, 14000, 4500)
    in_vib = st.slider("Vibration Index", 0.0, 1.0, 0.15)
    in_bat = st.slider("Battery Voltage", 10.0, 14.5, 12.6)

health_idx, alert_logs = evaluate_telemetry(in_temp, in_rpm, in_vib, in_bat)

col_a, col_b, col_c = st.columns([1, 2, 1])

with col_b:
    # Diagnostic Gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = health_idx,
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "#444"},
            'bar': {'color': "#00d4ff" if health_idx > 70 else "#ffaa00" if health_idx > 40 else "#ff1111"},
            'bgcolor': "#0a0a0a",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(255, 0, 0, 0.05)'},
                {'range': [70, 100], 'color': 'rgba(0, 212, 255, 0.05)'}]}))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#00d4ff", 'family': "Orbitron"})
    st.plotly_chart(fig, use_container_width=True)

with col_a:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("THERMAL", f"{in_temp}°C")
    st.metric("RPM", f"{in_rpm}")
    st.markdown('</div>', unsafe_allow_html=True)

with col_c:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("VIBRATION", f"{in_vib}G")
    st.metric("VOLTAGE", f"{in_bat}V")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.subheader("SYSTEM DIAGNOSTICS")
if not alert_logs:
    st.info("ALL PARAMETERS WITHIN OPERATIONAL TOLERANCE.")
else:
    for log in alert_logs:
        st.error(log)

st.markdown(f"<p style='text-align: right; color: #222; font-size: 10px;'>PRAV_MODULE_v1.0 | {datetime.now().strftime('%Y-%m-%d')}</p>", unsafe_allow_html=True)
