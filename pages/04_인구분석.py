import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="대한민국 인구 구조 분석", layout="wide")
st.title("📊 행정구역별 연령대별 인구수 분석기")

# 2. 데이터 로드 함수 (CP949 인코딩 처리)
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="cp949")
    return df

try:
    df = load_data()

    # 데이터 정제: 모든 숫자 컬럼에서 쉼표(,)를 제거하고 숫자로 변환
    for col in df.columns:
        if col != '행정구역':
            df[col] = df[col].astype(str).str.replace(',', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # 행정구역 목록 필터링 (구 단위만 추출, 전국/시도 단위 제외)
    # 데이터셋에 따라 조정될 수 있으나 일반적으로 '구'가 들어간 행정구역을 선택합니다.
    district_options = df[df['행정구역'].str.contains('구 ') | df['행정구역'].str.endswith('구')]['행정구역'].unique()
    if len(district_options) == 0:
        district_options = df['행정구역'].unique()

    # 연령대 컬럼 정의 (0~9세, 10~19세 ... 100세 이상 총 11개 구간)
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
    age_col_map = dict(zip(age_labels, age_columns))

    # 탭 메뉴 구성 (1. 구별 분석, 2. 연령대별 탑10 분석)
    tab1, tab2 = st.tabs(["📍 행정구별 인구 구조", "🏆 연령대별 인구 Top 10 지역"])

    # ----------------------------------------------------
    # TAB 1: 기존 행정구별 꺾은선 그래프
    # ----------------------------------------------------
    with tab1:
        st.header("지역별 연령대 분포 확인")
        selected_district = st.selectbox("분석할 행정구를 선택하세요:", district_options, key="tab1_select")
        
        # 선택된 구의 데이터 가져오기
        district_data = df[df['행정구역'] == selected_district].iloc[0]
        age_values = [district_data[col] for col in age_columns]
        
        total
