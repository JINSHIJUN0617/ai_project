import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="행정구역별 인구 구조 분석", layout="centered")
st.title("📊 행정구역별 연령대별 인구수 분석")

# 2. 데이터 로드 함수 (인코딩 오류 해결을 위해 cp949 적용)
@st.cache_data
def load_data():
    # 공공기관 CSV 파일은 주로 CP949(EUC-KR) 인코딩을 사용합니다.
    df = pd.read_csv("population.csv", encoding="cp949")
    return df

try:
    df = load_data()

    # 3. 행정구 목록 추출 (구 단위 필터링)
    # '구 '가 포함되어 있거나 '구'로 끝나는 행정구역을 필터링합니다.
    district_options = df[df['행정구역'].str.contains('구 ') | df['행정구역'].str.endswith('구')]['행정구역'].unique()
    
    if len(district_options) == 0:
        district_options = df['행정구역'].unique()

    # 4. 사이드바 또는 메인 화면에서 행정구 선택
    selected_district = st.selectbox("분석할 행정구를 선택하세요:", district_options)

    # 5. 선택된 행정구의 데이터 추출
    district_data = df[df['행정구역'] == selected_district].iloc[0]

    # 6. 연령대별 데이터 컬럼 추출 (총인구, 남, 여 제외한 '0~9세', '10~19세' 등만 선택)
    age_columns = [
        col for col in df.columns 
        if '거주자_' in col 
        and '세' in col 
        and '총인구수' not in col 
        and '연령구간' not in col 
        and '남_' not in col 
        and '여_' not in col
    ]
    
    # 가로축 라벨 (예: '0~9세') 및 세로축 데이터 추출
    age_labels = [col.split('_')[-1] for col in age_columns]
    
    # 숫자에 포함된 쉼표(,)를 제거하고 정수로 변환
    age_values = []
    for col in age_columns:
        val = str(district_data[col]).replace(',', '').strip()
        age_values.append(int(val) if val.isdigit() else 0)

    # 총 인구수 확보
    total_pop_col = [col for col in df.columns if '거주자_총인구수' in col][0]
    total_population = district_data[total_pop_col]

    # 지역 정보 출력
    st.subheader(f"📍 {selected_district}")
    st.metric(label="총 거주자 수", value=f"{total_population}명")

    # 7. Plotly를 이용한 꺾은선 그래프 생성 (한글 깨짐 방지 + 디자인)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=age_labels,
        y=age_values,
        mode='lines+markers',
        line=dict(color='red', width=3),               # 꺾은선 색상: 빨간색
        marker=dict(size=8, color='red'),
        name='인구수'
    ))

    # 그래프 레이아웃 설정 (회색 바탕 및 디자인 적용)
    fig.update_layout(
        xaxis_title="나이 (연령대)",
        yaxis_title="인구수 (명)",
        plot_bgcolor="#E5E5E5",                         # 그래프 내부 바탕색: 회색
        paper_bgcolor="#F0F2F6",                        # 그래프 외부 배경색
        font=dict(size=12, color="#333333"),            # 글로벌 폰트 설정
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(showgrid=True, gridcolor='white'),   # 격자선 설정
        yaxis=dict(showgrid=True, gridcolor='white')
    )

    # 스트림릿에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("📂 `population.csv` 파일을 찾을 수 없습니다. GitHub 저장소에 데이터 파일을 함께 업로드해 주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
