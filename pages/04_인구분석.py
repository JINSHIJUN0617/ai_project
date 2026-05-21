import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="대한민국 인구 구조 분석", layout="wide")
st.title("📊 행정구역별 연령대별 인구수 분석기")

# 2. 데이터 로드 함수
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="cp949")
    return df

try:
    df = load_data()

    # 데이터 정제 (쉼표 제거 후 정수 변환)
    for col in df.columns:
        if col != '행정구역':
            df[col] = df[col].astype(str).str.replace(',', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # 행정구역 목록 필터링
    district_options = df[df['행정구역'].str.contains('구 ') | df['행정구역'].str.endswith('구')]['행정구역'].unique()
    if len(district_options) == 0:
        district_options = df['행정구역'].unique()

    # 연령대 컬럼 정의
    age_columns = [
        col for col in df.columns 
        if '거주자_' in col 
        and '세' in col 
        and '총인구수' not in col 
        and '연령구간' not in col 
        and '남_' not in col 
        and '여_' not in col
    ]
    age_labels = [col.split('_')[-1] for col in age_columns]
    
    # 딕셔너리 생성 시 컴프리헨션 대신 일반 반복문으로 안정성 확보
    age_col_map = {}
    for label, col in zip(age_labels, age_columns):
        age_col_map[label] = col

    # 탭 메뉴 구성
    tab1, tab2 = st.tabs(["📍 행정구별 인구 구조", "🏆 연령대별 인구 Top 10 지역"])

    # ----------------------------------------------------
    # TAB 1: 행정구별 꺾은선 그래프
    # ----------------------------------------------------
    with tab1:
        st.header("지역별 연령대 분포 확인")
        selected_district = st.selectbox("분석할 행정구를 선택하세요:", district_options, key="tab1_select")
        
        district_data = df[df['행정구역'] == selected_district].iloc[0]
        age_values = [int(district_data[col]) for col in age_columns]
        
        total_pop_col = [col for col in df.columns if '거주자_총인구수' in col][0]
        total_population = int(district_data[total_pop_col])

        st.metric(label=f"{selected_district} 총 거주자 수", value=f"{total_population:,}명")

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=age_labels, 
            y=age_values, 
            mode='lines+markers',
            line=dict(color='red', width=3),
            marker=dict(size=8, color='red'),
            name='인구수'
        ))
        fig1.update_layout(
            xaxis_title="나이 (연령대)", 
            yaxis_title="인구수 (명)",
            plot_bgcolor="#E5E5E5", 
            paper_bgcolor="#F0F2F6",
            font=dict(size=12, color="#333333"),
            xaxis=dict(showgrid=True, gridcolor='white'),
            yaxis=dict(showgrid=True, gridcolor='white')
        )
        st.plotly_chart(fig1, use_container_width=True)

    # ----------------------------------------------------
    # TAB 2: 연령대별 Top 10 행정구 분석
    # ----------------------------------------------------
    with tab2:
        st.header("특정 연령대가 가장 많은 상위 10개 지역 비교")
        
        selected_age_label = st.selectbox("나이대를 선택하세요 (10살 간격):", age_labels, key="tab2_select")
        selected_age_col = age_col_map[selected_age_label]

        filtered
