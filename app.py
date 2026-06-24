import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import time

# 1. Page Layout Optimization
st.set_page_config(layout="wide", page_title="XAUUSD Pure Live Flow")

# Mobile Screen Background Tweak
st.markdown("<style>.reportview-container { background: #0B0E11; }</style>", unsafe_allow_html=True)
st.title("📊 Gold Live Order Flow Terminal")

# Sidebar Dynamic Control Bars
st.sidebar.header("⚙️ Controls")
timeframe = st.sidebar.selectbox("Timeframe", options=["1 Minute", "5 Minutes", "1 Hour"], index=0)
show_footprint = st.sidebar.checkbox("Show Bid/Ask Numbers", value=True)
show_bubbles = st.sidebar.checkbox("Show Big Volume Bubbles", value=True)

# ==========================================
# 2. REAL-TIME DATA TICK GENERATOR ENGINE
# ==========================================
# Yeh function dynamic system timestamp use karke live updates simulate karta hai
now = datetime.datetime.now()

def generate_live_ticks():
    periods = 8
    # System clocks are used to shift arrays dynamically
    slots = pd.date_range(end=now, periods=periods, freq='min')
    
    # Standard stable Gold base levels
    opens = [2342.0, 2343.5, 2341.0, 2344.2, 2343.0, 2345.1, 2344.0, 2346.2]
    
    # Adding artificial instant current tick volatility variations
    live_variation = np.random.uniform(-1.5, 1.5)
    opens[-1] = opens[-1] + live_variation 
    
    closes = [o + np.random.uniform(-1.2, 1.2) for o in opens]
    highs = [max(o, c) + np.random.uniform(0.3, 1.0) for o, c in zip(opens, closes)]
    lows = [min(o, c) - np.random.uniform(0.3, 1.0) for o, c in zip(opens, closes)]
    
    return pd.DataFrame({'Datetime': slots, 'Open': opens, 'High': highs, 'Low': lows, 'Close': closes})

df = generate_live_ticks()

# Processing Footprint Levels Inside Matrices
plot_data = []
bx, by, btext, bsize = [], [], [], []
tick_step = 0.5 

for i, row in df.iterrows():
    t = row['Datetime']
    prices = np.arange(round(row['Low'], 1), round(row['High'], 1) + tick_step, tick_step)
    
    for p in prices:
        p = round(p, 1)
        bid = np.random.randint(60, 480)
        ask = np.random.randint(60, 480)
        total_vol = bid + ask
        
        plot_data.append({'x': t, 'y': p, 'text': f"{bid}x{ask}"})
        
        if total_vol > 760: # Institutional threshold limit
            bx.append(t)
            by.append(p)
            btext.append(f"Block Vol: {total_vol}")
            bsize.append(total_vol / 14)

# ==========================================
# 3. GRAPH BUILDER (STANDARD RED/GREEN THEME)
# ==========================================
fig = go.Figure()

# Standard Candle Representations
fig.add_trace(go.Candlestick(
    x=df['Datetime'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
    increasing_line_color='#26a69a', decreasing_line_color='#ef5350', # Standard Green & Red
    name='Gold Price', opacity=0.2
))

# Standard Translucent Purple Big Trade Circles Overlay
if show_bubbles and bx:
    fig.add_trace(go.Scatter(
        x=bx, y=by, mode='markers',
        marker=dict(size=bsize, color='purple', line=dict(width=1, color='#FFFFFF')),
        text=btext, name='Big Volumes', hoverinfo='text'
    ))

# Basic Simple Colored Grid Clusters Injection
if show_footprint:
    for node in plot_data:
        # Standard Clean Red or Green text color logic based on numbers matrix
        is_buy_heavy = int(node['text'].split('x')[1]) > int(node['text'].split('x')[0])
        text_color = "#26a69a" if is_buy_heavy else "#ef5350" # Pure Basic Trading Green/Red
        
        fig.add_annotation(
            x=node['x'], y=node['y'], text=node['text'], showarrow=False,
            font=dict(size=8, color=text_color, family="Arial Black"),
            bgcolor="rgba(20, 25, 30, 0.95)", bordercolor="rgba(255,255,255,0.06)", borderwidth=1
        )

# Layout adjustments for optimal sliding view grids on phones
fig.update_layout(
    template="plotly_dark", paper_bgcolor="#0B0E11", plot_bgcolor="#0B0E11",
    xaxis_rangeslider_visible=False, height=650,
    margin=dict(l=5, r=5, t=30, b=5), dragmode='pan'
)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.02)", side="right")

# Displaying dynamic chart element
st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 4. TRADINGVIEW AUTO-REFRESH TRIGGER
# ==========================================
# Loop execution triggers auto rerun every 2 seconds for continuous candle animations
time.sleep(2)
st.rerun()
