import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import altair as alt
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Home import vehicle_onoff, vehicle_stop, display_dial


def main(selected_data, stop_data):
    # Present chart
    st.subheader("운행회차별 재차인원")
    st.text(f"선택한 범위 내의 {line_num} 운행회차별 개별 정류소의 재차인원입니다.")
    st.altair_chart(vehicle_onoff(selected_data, 'single', '정류소순번', '인원', '누적인원'), use_container_width=True)

    st.subheader("정류소별 평균재차인원")
    st.text(f"선택한 범위 내의 {line_num} 정류소별 평균재차인원입니다.")
    st.altair_chart(vehicle_stop(stop_data), use_container_width=True)

# Set control box
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    line_num = st.selectbox(
        "노선 선택", ("관악02", "5511")
    )

if (line_num == "관악02"):
    with col2:
        cycle_start = st.number_input(
            "**운행회차(시작)**", 1, 18, 1
        )
else:
    with col2:
        cycle_start = st.number_input(
            "**운행회차(시작)**", 1, 10, 1
        )    

if (line_num == "관악02"):
    with col3:
        cycle_end = st.number_input(
            "**운행회차(끝)**", 1, 18, 18
        )
else:
    with col3:
        cycle_end = st.number_input(
            "**운행회차(끝)**", 1, 10, 10
        )    

# Prepare data
veh_onb = pd.read_csv('dataset/veh_onthebus.csv', encoding='cp949')

selected_data = veh_onb[veh_onb["노선번호"] == line_num]
selected_data = selected_data[selected_data["운행회차"] >= cycle_start]
selected_data = selected_data[selected_data["운행회차"] <= cycle_end]

f2 = {'인원' : 'sum'}
g2 = selected_data.groupby(['정류소번호명'])
v2 = g2.agg(f2)
stop_data = pd.concat([v2], 1)
stop_data = stop_data.sort_values('정류소번호명')
stop_data = stop_data.reset_index()
stop_data['인원'] = (stop_data['인원'] / 18)

# Body
st.title('# 버스노선 재차현황')
main(selected_data, stop_data)

with st.expander("Raw data 보기", expanded=False):

    st.markdown("## Raw data")
    st.markdown("")

    def draw_veh_onb(df):
        df = df.sort_values(by="정류소순번", ascending=True)
        df
        " "
    if st.checkbox("운행회차 및 정류소별 재차인원"):
        draw_veh_onb(selected_data[['노선번호', '정류소순번', '회차', '정류소번호명', '인원']])

    def draw_stop_data(df):
        df = df.sort_values(by="정류소번호명", ascending=True)
        df
        " "
    if st.checkbox("정류소별 평균재차인원"):
        draw_stop_data(stop_data)
