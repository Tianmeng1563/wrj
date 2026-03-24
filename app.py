import streamlit as st
import time
import random
from datetime import datetime
import pandas as pd

st.title("无人机通信心跳监测可视化")

# 初始化会话状态
if "data" not in st.session_state:
    st.session_state.data = []
if "last_time" not in st.session_state:
    st.session_state.last_time = time.time()
if "running" not in st.session_state:
    st.session_state.running = False

def send_heartbeat():
    """发送心跳包，记录数据"""
    now = time.time()
    # 直接使用当前数据长度作为序号
    seq = len(st.session_state.data) + 1
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # 追加字典，包含序号、时间、状态
    st.session_state.data.append({
        "序号": seq,
        "时间": timestamp,
        "状态": "正常"
    })
    st.session_state.last_time = now

def check_disconnect():
    """检查是否掉线"""
    return time.time() - st.session_state.last_time > 3

# UI 布局
col1, col2 = st.columns(2)
with col1:
    if st.button("开始监测"):
        st.session_state.running = True
        # 重置时间，防止点击开始前就误判掉线
        st.session_state.last_time = time.time()
with col2:
    if st.button("停止监测"):
        st.session_state.running = False

# 监测逻辑
if st.session_state.running:
    send_heartbeat()
    # 模拟随机延迟（10%概率卡住4秒）
    if random.random() < 0.1:
        time.sleep(4)

# 显示状态
if check_disconnect():
    st.error("⚠️ 无人机掉线！3秒未收到心跳包")
else:
    st.success("✅ 心跳正常")

# 可视化数据
# 只有在有数据的情况下才画图
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.subheader("心跳时序图")
    # 画图时确保列名正确
    st.line_chart(df.set_index("时间")["序号"])
    st.subheader("心跳数据")
    st.dataframe(df)
