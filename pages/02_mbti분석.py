import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="Global MBTI Explorer", layout="wide")
st.title("🌍 국가별 MBTI 분포 데이터")
st.markdown("국가를 선택하면 해당 국가의 MBTI 비율을 확인할 수 있습니다.")

# 2. 가상 데이터 생성 (실제 데이터로 교체 가능)
data = {
    "Korea": {"INFP": 15, "ENFP": 13, "INFJ": 12, "ISFJ": 10, "ISTJ": 9, "ENFJ": 8, "INTP": 7, "ENTP": 6, "ESFJ": 5, "ISFP": 4, "ESTJ": 3, "ISTP": 2, "ENTJ": 2, "ESFP": 2, "ESTP": 1, "INTJ": 1},
    "USA": {"INFP": 8, "ENFP": 10, "INFJ": 5, "ISFJ": 14, "ISTJ": 15, "ENFJ": 4, "INTP": 6, "ENTP": 7, "ESFJ": 12, "ISFP": 5, "ESTJ": 6, "ISTP": 3, "ENTJ": 2, "ESFP": 1, "ESTP": 1, "INTJ": 1},
    "Japan": {"INFP": 10, "ENFP": 8, "INFJ": 7, "ISFJ": 18, "ISTJ": 16, "ENFJ": 3, "INTP": 5, "ENTP": 4, "ESFJ": 10, "ISFP": 9, "ESTJ": 4, "ISTP": 2, "ENTJ": 1, "ESFP": 1, "ESTP": 1, "INTJ": 1}
}

# 3. 사이드바 - 국가 선택
selected_country = st.sidebar.selectbox("분석할 국가를 선택하세요", list(data.keys()))

# 4. 데이터 가공
country_data = data[selected_country]
df = pd.DataFrame(list(country_data.items()), columns=['MBTI', 'Percentage'])
df = df.sort_values(by='Percentage', ascending=False) # 비율순 정렬

# 5. 시각화 설정 (1등은 빨강, 나머지는 파랑 그라데이션)
colors = ['#EF553B'] + [
    f'rgba(0, 102, 204, {max(0.2, 1 - (i / len(df)))})' 
    for i in range(1, len(df))
]

# 6. Plotly 차트 생성
fig = go.Figure(data=[go.Bar(
    x=df['MBTI'],
    y=df['Percentage'],
    marker_color=colors,
    text=df['Percentage'].apply(lambda x: f'{x}%'),
    textposition='auto',
])

fig.update_layout(
    title=f"<b>{selected_country}</b> MBTI 유형별 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    template="plotly_white",
    hovermode="x unified",
    yaxis=dict(range=[0, max(df['Percentage']) + 5])
)

# 7. 스트림릿에 출력
st.plotly_chart(fig, use_container_width=True)

# 데이터 표 보기 (선택 사항)
if st.checkbox("원천 데이터 보기"):
    st.table(df)
