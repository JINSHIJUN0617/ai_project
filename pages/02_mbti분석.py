import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="Global MBTI Dashboard", layout="wide")

@st.cache_data
def load_data():
    # 데이터 로드
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

try:
    df = load_data()

    st.title("🌍 국가별 MBTI 분포 탐색기")
    st.markdown("데이터에서 국가를 선택하면 해당 국가의 MBTI 유형별 비율을 확인할 수 있습니다.")

    # 1. 국가 선택 셀렉트박스
    countries = df['Country'].unique()
    selected_country = st.selectbox("분석할 국가를 선택하세요", countries)

    # 2. 선택된 국가 데이터 추출 및 재구조화
    country_data = df[df['Country'] == selected_country].drop(columns=['Country']).T
    country_data.columns = ['Percentage']
    country_data = country_data.sort_values(by='Percentage', ascending=False).reset_index()
    country_data.columns = ['MBTI', 'Percentage']

    # 3. 색상 설정 (1위는 빨강, 나머지는 파란색 그라데이션)
    # Plotly의 시퀀셜 컬러차트를 활용하여 데이터 개수만큼 색상 추출
    colors = ['#EF553B'] + px.colors.sequential.Blues_r[2:17] 
    # 데이터 행 수에 맞춰 색상 리스트 길이 조정
    final_colors = colors[:len(country_data)]

    # 4. 플로틀리 차트 생성
    fig = go.Figure(data=[
        go.Bar(
            x=country_data['MBTI'],
            y=country_data['Percentage'],
            marker_color=final_colors,
            text=country_data['Percentage'].apply(lambda x: f'{x*100:.1f}%'),
            textposition='auto',
        )
    ])

    fig.update_layout(
        title=f"<b>{selected_country}</b>의 MBTI 유형 분포 (높은 순)",
        xaxis_title="MBTI 유형",
        yaxis_title="비율 (1.0 = 100%)",
        template="plotly_white",
        height=600,
        yaxis=dict(tickformat=".0%")
    )

    # 5. 스트림릿에 출력
    st.plotly_chart(fig, use_container_width=True)

    # 6. 상세 데이터 표
    with st.expander("상세 데이터 보기"):
        st.dataframe(country_data.style.format({'Percentage': '{:.2%}'}))

except FileNotFoundError:
    st.error("파일을 찾을 수 없습니다. 'countriesMBTI_16types.csv' 파일이 같은 경로에 있는지 확인해주세요.")
