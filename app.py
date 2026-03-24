import streamlit as st
import time
import random
from datetime import datetime
import pandas as pd

st.title("无人机通信心跳监测可视化")

if "data" not in st.session_state:
    st.session_state.data = []
if "last_time" not in st.session_state:
    st.session_state.last_time = time.time()

def send_heartbeat():
    now = time.time()
    seq = len(st.session_state.data) + 1
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.data.append({
        "序号": seq,
        "时间": timestamp,
        "状态": "正常"
    })
    st.session_state.last_time = now

def check_disconnect():
    return time.time() - st.session_state.last_time > 3

if "running" not in st.session_state:
    st.session_state.running = False

col1, col2 = st.columns(2)
with col1:
    if st.button("开始监测"):
        st.session_state.running = True
with col2:
    if st.button("停止监测"):
        st.session_state.running = False

if st.session_state.running:
    send_heartbeat()
    if random.random() < 0.1:
        time.sleep(4)

if check_disconnect():
    st.error("⚠️ 无人机掉线！3秒未收到心跳包")
else:
    st.success("✅ 心跳正常")

df = pd.DataFrame(st.session_state.data)
st.subheader("心跳时序图")
st.line_chart(df.set_index("时间")["序号"])
st.subheader("心跳数据")
st.dataframe(df)
