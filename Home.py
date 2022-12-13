import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import altair as alt
from htbuilder import div, big, h2, styles
from htbuilder.units import rem
from PIL import Image

def vehicle_onoff(source, count_type, x, y, z):
    hover = alt.selection_single(
        fields=[x],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    if count_type == 'single': 
        lines = (
            alt.Chart(source)
            .mark_line(point="transparent")
            .encode(x=x, y=y, color='회차')
        )
    else:
        lines = (
            alt.Chart(source)
            .mark_line(point="transparent")
            .encode(x=x, y=z, color=alt.Color(value="#00C0F2"))
        )       

    points = (
        lines.transform_filter(hover)
        .mark_circle(size=65)
    )

    tooltips = (
        alt.Chart(source)
        .mark_rule(opacity=0)
        .encode(
            x=x,
            y=y,
            tooltip=[
                alt.Tooltip("운행회차", title="운행회차"),
                alt.Tooltip("운행출발일시", title="운행출발일시"),
                alt.Tooltip("정류소명", title="정류소명"),
                alt.Tooltip("인원", title="인원")
            ]
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()

def vehicle_stop(source):
    bars = (
        alt.Chart(source)
        .mark_bar()
        .encode(
            x='인원:Q',
            y=alt.Y('정류소번호명:N', sort=alt.EncodingSortField(field="정류소번호명", order='ascending')),
            color=alt.Color(value="#1C83E1"),
        )
    )

    return bars

def display_dial(title, value, color):
    dials = st.markdown(
        div(
            style=styles(
                text_align="center",
                color=color,
                padding=(rem(0.8), 0, rem(3), 0),
            )
        )(
            h2(style=styles(font_size=rem(0.8), font_weight=600, padding=0))(title),
            big(style=styles(font_size=rem(3), font_weight=800, line_height=1))(
                value
            ),
        ),
        unsafe_allow_html=True,
    )

    return dials


st.title('# 서울대학교 통행버스 이용현황')
st.markdown('- **데이터셋**: 하루 동안의 교통카드 트랜잭션 데이터 (노선별, 정류장별)')
st.markdown('- **버스노선**: 관악02, 5511, 5513, 5516 ([노선도](https://me.snu.ac.kr/ko/location_bus))')
image = Image.open('img/map.gif')
st.image(image)
st.markdown('#### 1. 승차현황')
st.markdown('- 운행회차 및 정류소별 승차인원')
st.markdown('- 운행회차에 따른 누적승차인원')
st.markdown('- 정류소별 누적승차인원')
st.markdown('#### 2. 하차현황')
st.markdown('- 운행회차 및 정류소별 하차인원')
st.markdown('- 운행회차에 따른 누적하차인원')
st.markdown('- 정류소별 누적승차인원')
st.markdown('#### 3. 재차현황')
st.markdown('- 운행회차 및 정류소별 재차인원')
st.markdown('- 정류소별 평균재차인원')
st.markdown('#### 4. 차량별 혼잡도')
st.markdown('- 버스노선별 이용현황')
st.markdown('***')
st.markdown('©그룹 19')
st.markdown('김민창, 박성용, 최진우')
