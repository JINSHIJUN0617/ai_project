import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 페이지 설정
st.set_page_config(page_title="국가별 MBTI 분석", layout="wide")

# 데이터 로드 함수 (파일 경로 오류 방지)
@st.cache_data
def load_data():
    file_name = 'countriesMBTI_16types.csv'
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        st.error(f"⚠️ '{file_name}' 파일을 찾을 수 없습니다. GitHub 저장소에 파일이 있는지 확인해주세요.")
        return None

df = load_data()

if df is not None:
    st.title("📊 국가별 MBTI 분포 시각화")
    st.info("국가를 선택하면 실시간으로 해당 국가의 MBTI 비중을 분석합니다.")

    # 사이드바에서 국가 선택
    countries = sorted(df['Country'].unique())
    selected_country = st.selectbox("분석하고 싶은 국가를 선택하세요", countries)

    # 선택된 국가 데이터 정리 (비율 높은 순)
    row = df[df['Country'] == selected_country].drop(columns=['Country']).iloc[0]
    viz_df = row.reset_index()
    viz_df.columns = ['MBTI', 'Ratio']
    viz_df = viz_df.sort_values(by='Ratio', ascending=False)

    # 색상 설정 (1등은 빨간색, 나머지는 파란색 그라데이션)
    # n개의 파란색 계열 색상 추출
    n_types = len(viz_df)
    blue_colors = px.colors.sequential.Blues_r[2:12] # 진한 파랑 계열
    # 1등을 위한 빨간색 + 나머지 파란색 리스트 생성
    colors = ['#FF4B4B'] + [blue_colors[i % len(blue_colors)] for i in range(n_types - 1)]

    # Plotly 차트 생성
    fig = go.Figure(data=[
        go.Bar(
            x=viz_df['MBTI'],
            y=viz_df['Ratio'],
            marker_color=colors,
            text=viz_df['Ratio'].apply(lambda x: f'{x*100:.1f}%'),
            textposition='outside',
            hovertemplate='MBTI: %{x}<br>비중: %{y:.2%}<extra></extra>'
        )
    ])

    fig.update_layout(
        title=dict(text=f"<b>{selected_country}</b>의 MBTI 유형별 점유율", font=dict(size=20)),
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        yaxis=dict(tickformat=".0%"),
        height=550,
        margin=dict(l=20, r=20, t=60, b=20),
        template="plotly_white"
    )

    # 차트 출력
    st.plotly_chart(fig, use_container_width=True)

    # 하단 데이터 요약
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ 주요 특징")
        top_type = viz_df.iloc[0]['MBTI']
        top_val = viz_df.iloc[0]['Ratio']
        st.write(f"**{selected_country}**에서 가장 흔한 유형은 **{top_type}**이며, 전체의 **{top_val:.1%}.**를 차지합니다.")
    
    with col2
