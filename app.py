import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Mobile screen size configurations
st.set_page_config(layout="wide", page_title="Gold Order Flow")

st.title("⭐ ATAS Gold Order Flow Terminal (XAUUSD) ⭐")

# 1. Generating Accurate Gold Mock Data
np.random.seed(42)
time_slots = pd.date_range(start="2026-06-24 10:00", periods=6, freq="min")

open_p  = [2340.0, 2341.5, 2343.0, 2342.2, 2344.0, 2343.1]
high_p  = [2342.5, 2343.0, 2344.5, 2344.0, 2346.0, 2345.0]
low_p   = [2339.0, 2340.5, 2341.5, 2341.0, 2342.5, 2342.0]
close_p = [2341.5, 2343.0, 2342.2, 2344.0, 2343.1, 2345.5]

df = pd.DataFrame({
    'Datetime': time_slots, 'Open': open_p, 'High': high_p, 'Low': low_p, 'Close': close_p
})

plot_data = []
bubble_x, bubble_y, bubble_text, bubble_size = [], [], [], []
tick_step = 0.5 

for i, row in df.iterrows():
    t = row['Datetime']
    prices = np.arange(round(row['Low'], 1), round(row['High'], 1) + tick_step, tick_step)
    
    for p in prices:
        p = round(p, 1)
        bid = np.random.randint(50, 490)
        ask = np.random.randint(50, 490)
        total_vol = bid + ask
        
        plot_data.append({'x': t, 'y': p, 'text': f"{bid}x{ask}"})
        
        # Big volume bubble trigger (> 750 contracts)
        if total_vol > 750:
            bubble_x.append(t)
            bubble_y.append(p)
            bubble_text.append(f"🐳 Big Trade Vol: {total_vol}")
            bubble_size.append(total_vol / 15)

# 2. Building Interactive Plotly Chart
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df['Datetime'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
    name='Candles', opacity=0.15
))

fig.add_trace(go.Scatter(
    x=bubble_x, y=bubble_y, mode='markers',
    marker=dict(size=bubble_size, color='rgba(156, 39, 176, 0.7)', line=dict(width=1, color='#FFFFFF')),
    text=bubble_text, name='Big Trades Tracker', hoverinfo='text'
))

for node in plot_data:
    fig.add_annotation(
        x=node['x'], y=node['y'], text=node['text'], showarrow=False,
        font=dict(size=8, color="#00FF66" if "6" in node['text'] else "#FF5252", family="Courier New"),
        bgcolor="rgba(10, 15, 20, 0.9)", bordercolor="rgba(255,255,255,0.05)", borderwidth=1
    )

fig.update_layout(
    template="plotly_dark", paper_bgcolor="#0A0F14", plot_bgcolor="#0A0F14",
    xaxis_rangeslider_visible=False, height=650, margin=dict(l=5, r=5, t=40, b=5)
)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.03)")

# Streamlit responsive display
st.plotly_chart(fig, use_container_width=True)
