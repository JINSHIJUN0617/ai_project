import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Population Analysis", layout="wide")
st.title("📊 행정구역별 연령대별 인구수 분석기")

@st.cache_data
def load_data():
    # 가장 안전하게 인코딩 에러를 무시하거나 대체하여 읽어옵니다.
    return pd.read_csv("population.csv", encoding="cp949", errors="replace")

try:
    df = load_data()

    # 데이터 내 모든 숫자의 쉼표 정제
    for col in df.columns:
        if col != "행정구역":
            df[col] = df[col].astype(str).str.replace(",", "").str.strip()
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # 행정구역 목록 추출
    raw_options = df["행정구역"].unique()
    district_options = [x for x in raw_options if "구 " in x or x.endswith("구")]
    if not district_options:
        district_options = list(raw_options)

    # 연령대 컬럼 정의 (0~9세, 10~19세 등)
    age_columns = [
        c for c in df.columns 
        if "거주자_" in c and "세" in c and "총인구수" not in c and "연령구간" not in c and "남_" not in c and "여_" not in c
    ]
    age_labels = [c.split("_")[-1] for c in age_columns]
    
    age_col_map = {}
    for l, c in zip(age_labels, age_columns):
        age_col_map[l] = c

    # 탭 구성
    tab1, tab2 = st.tabs(["📍 행정구별 인구 구조", "🏆 연령대별 인구 Top 10 지역"])

    # TAB 1: 행정구별 꺾은선 그래프
    with tab1:
        st.header("지역별 연령대 분포 확인")
        selected_district = st.selectbox("분석할 행정구를 선택하세요:", district_options, key="sb_tab1")
        
        district_data = df[df["행정구역"] == selected_district].iloc[0]
        age_values = [int(district_data[c]) for c in age_columns]
        
        total_pop_col = [c for c in df.columns if "거주자_총인구수" in c][0]
        total_population = int(district_data[total_pop_col])

        st.metric(label="총 거주자 수", value=f"{total_population:,}명")

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=age_labels, 
            y=age_values, 
            mode="lines+markers",
            line=dict(color="red", width=3),
            marker=dict(size=8, color="red"),
            name="인구수"
        ))
        fig1.update_layout(
            xaxis_title="나이 (연령대)", 
            yaxis_title="인구수 (명)",
            plot_bgcolor="#E5E5E5", 
            paper_bgcolor="#F0F2F6",
            font=dict(size=12, color="#333333"),
            xaxis=dict(showgrid=True, gridcolor="white"),
            yaxis=dict(showgrid=True, gridcolor="white")
        )
        st.plotly_chart(fig1, use_container_width=True)

    # TAB 2: 연령대별 Top 10 행정구 분석
    with tab2:
        st.header("특정 연령대가 가장 많은 상위 10개 지역 비교")
        
        selected_age_label = st.selectbox("나이대를 선택하세요 (10살 간격):", age_labels, key="sb_tab2")
        selected_age_col = age_col_map[selected_age_label]

        filtered_df = df[df["행정구역"].isin(district_options)].copy()
        top10_df = filtered_df.sort_values(by=selected_age_col, ascending=False).head(10)

        fig2 = go.Figure()
        top10_list = top10_df.to_dict("records")
        
        for rank, row in enumerate(top10_list, start=1):
            raw_name = str(row["행정구역"])
            clean_name = raw_name.split("(")[0].strip()
            row_age_values = [int(row[c]) for c in age_columns]
            
            if rank == 1:
                line_style = dict(color="red", width=4)
                name_label = "1위: " + clean_name
            else:
                line_style = dict(width=2)
                name_label = str(rank) + "위: " + clean_name

            fig2.add_trace(go.Scatter(
                x=age_labels,
                y=row_age_values,
                mode="lines+markers",
                line=line_style,
                marker=dict(size=6),
                name=name_label
            ))

        fig2.update_layout(
            xaxis_title="나이 (연령대)",
            yaxis_title="인구수 (명)",
            plot_bgcolor="#E5E5E5",
            paper_bgcolor="#F0F2F6",
            font=dict(size=12, color="#333333"),
            hovermode="x unified",
            xaxis=dict(showgrid=True, gridcolor="white"),
            yaxis=dict(showgrid=True, gridcolor="white"),
            legend=dict(title="행정구역 순위", orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
        )
        st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"오류가 발생했습니다: {str(e)}")
