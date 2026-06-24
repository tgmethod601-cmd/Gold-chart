import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go

# 1. Premium Mobile Layout Configuration
st.set_page_config(layout="wide", page_title="XAUUSD Live Order Flow")

# Custom Dark CSS for ATAS / TradingView Premium Feeling
st.markdown("""
    <style>
    .reportview-container { background: #0A0F14; }
    .stCheckbox { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦅 Real-Time Gold Order Flow Engine (TradingView Style)")

# ==========================================
# 2. SIDEBAR CONTROLS (TRADINGVIEW CONTROLS)
# ==========================================
st.sidebar.header("⚙️ Chart Settings")

# Timeframe Selector like TradingView
timeframe = st.sidebar.selectbox(
    "Select Timeframe",
    options=["1 Minute", "5 Minutes", "15 Minutes", "1 Hour"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.header("🛠️ Indicators Panel")

# User can dynamically turn indicators ON or OFF himself
show_footprint = st.sidebar.checkbox("Show Bid/Ask Footprint Numbers", value=True)
show_bubbles = st.sidebar.checkbox("Show Institutional Volume Bubbles", value=True)

# User adjustable bubble threshold sensitivity
bubble_threshold = st.sidebar.slider("Bubble Volume Sensitivity", min_value=500, max_value=1500, value=750, step=50)

# Refresh Button for Live Feed Tick updates
if st.sidebar.button("🔄 Refresh Live Market Data"):
    st.rerun()

# ==========================================
# 3. LIVE DATA SIMULATOR (HIGH INTENSITY SECONDS DATA)
# ==========================================
# Generates live data mimicking current time engine
now = datetime.datetime.now()
tf_map = {"1 Minute": "1min", "5 Minutes": "5min", "15 Minutes": "15min", "1 Hour": "1h"}

@st.cache_data(ttl=2) # Auto clears cache every 2 seconds for live tick updates
def get_live_gold_data(tf):
    np.random.seed(int(now.strftime("%s")) // 60) # Live seed rotates every minute
    periods = 10
    slots = pd.date_range(end=now, periods=periods, freq='min' if tf=="1 Minute" else '5min')
    
    # Gold baseline spot price
    base_price = 2345.0
    opens = [base_price + np.random.uniform(-3, 3) for _ in range(periods)]
    closes = [o + np.random.uniform(-2, 2) for o in opens]
    highs = [max(o, c) + np.random.uniform(0.5, 2) for o, c in zip(opens, closes)]
    lows = [min(o, c) - np.random.uniform(0.5, 2) for o, c in zip(opens, closes)]
    
    return pd.DataFrame({'Datetime': slots, 'Open': opens, 'High': highs, 'Low': lows, 'Close': closes})

df = get_live_gold_data(timeframe)

# Process footprints inside data matrix
plot_data = []
bx, by, btext, bsize = [], [], [], []
tick_step = 0.5

for i, row in df.iterrows():
    t = row['Datetime']
    prices = np.arange(round(row['Low'], 1), round(row['High'], 1) + tick_step, tick_step)
    
    for p in prices:
        p = round(p, 1)
        bid = np.random.randint(60, 600)
        ask = np.random.randint(60, 600)
        total_vol = bid + ask
        
        plot_data.append({'x': t, 'y': p, 'text': f"{bid}x{ask}"})
        
        if total_vol > bubble_threshold:
            bx.append(t)
            by.append(p)
            btext.append(f"🐳 Institutional Block: {total_vol}")
            bsize.append(total_vol / 12)

# ==========================================
# 4. TRADINGVIEW / ATAS INTERACTIVE PLOT
# ==========================================
fig = go.Figure()

# Base Candlestick Structure
fig.add_trace(go.Candlestick(
    x=df['Datetime'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
    name=f'XAUUSD {timeframe}', opacity=0.25
))

# CONDITIONAL ADDITION: Big Volume Bubbles Indicator
if show_bubbles and bx:
    fig.add_trace(go.Scatter(
        x=bx, y=by, mode='markers',
        marker=dict(size=bsize, color='rgba(156, 39, 176, 0.75)', line=dict(width=1.5, color='#FFFFFF')),
        text=btext, name='Big Volume Bubbles', hoverinfo='text'
    ))

# CONDITIONAL ADDITION: Footprint Cluster Overlay
if show_footprint:
    for node in plot_data:
        fig.add_annotation(
            x=node['x'], y=node['y'], text=node['text'], showarrow=False,
            font=dict(size=8, color="#00FF66" if "8" in node['text'] else "#FF5252", family="Courier New"),
            bgcolor="rgba(10, 15, 20, 0.92)", bordercolor="rgba(255,255,255,0.06)", borderwidth=1
        )

# Layout Configurations for smooth dragging/zooming on phones
fig.update_layout(
    template="plotly_dark", paper_bgcolor="#0A0F14", plot_bgcolor="#0A0F14",
    xaxis_rangeslider_visible=False, height=700,
    margin=dict(l=10, r=10, t=30, b=10),
    dragmode='pan' # Multi-touch pinch zoom support for mobile screens
)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.03)", side="right") # TradingView style right-side axis

# Render Chart inside Streamlit platform
st.plotly_chart(fig, use_container_width=True)
