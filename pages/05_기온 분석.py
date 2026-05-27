import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="서울 기온 역사 데이터 분석", layout="centered")
st.title("📅 서울 연도별 특정 날짜 기온 추이 분석")
st.write("1907년부터 2018년까지, 선택하신 날짜의 최고/최저 기온 변화를 확인해보세요.")

# 2. 데이터 로드 및 전처리 (캐싱 적용으로 속도 향상)
@st.cache_data
def load_data():
    # 데이터 읽기
    df = pd.read_csv("seoul.csv")
    
    # 컬럼명 공백 제거 및 날짜 데이터 전처리 (\t 제거)
    df.columns = df.columns.str.strip()
    df['날짜'] = df['날짜'].astype(str).str.replace('\t', '').str.strip()
    
    # 결측치 제거 (기온 데이터가 없는 행 삭제)
    df = df.dropna(subset=['최고기온(℃)', '최저기온(℃)'])
    
    # 날짜 데이터 타입을 datetime으로 변경 후 연, 월, 일 분리
    df['날짜_dt'] = pd.to_datetime(df['날짜'], errors='coerce')
    df = df.dropna(subset=['날짜_dt']) # 변환 실패 데이터 제거
    
    df['연도'] = df['날짜_dt'].dt.year
    df['월'] = df['날짜_dt'].dt.month
    df['일'] = df['날짜_dt'].dt.day
    
    return df

try:
    df = load_data()

    # 3. 사이드바 - 월/일 선택 UI 구현
    st.sidebar.header("📅 날짜 선택")
    selected_month = st.sidebar.selectbox("월을 선택하세요", list(range(1, 13)), index=9) # 기본값 10월
    
    # 선택한 월에 맞는 일 수 계산 (2월 윤년 고려하여 안전하게 31일까지 제공 후 필터링)
    available_days = sorted(df[df['월'] == selected_month]['일'].unique())
    selected_day = st.sidebar.selectbox("일을 선택하세요", available_days, index=0)

    # 4. 데이터 필터링
    filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

    if filtered_df.empty:
        st.warning("선택하신 날짜에 해당하는 데이터가 없습니다.")
    else:
        st.subheader(f"📊 {selected_month}월 {selected_day}일의 연도별 기온 변화")
        
        # 5. 그래프 그리기 (스트림릿 클라우드 내 기본 한글 폰트 적용을 위해 내장 폰트 사용 안 함)
        # 웹 앱 환경에서 깨짐을 방지하기 위해 폰트 독립적인 차트 스타일이나 영문 라벨 병기 추천
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # 핫핑크, 연한 파란색(sky blue) 적용
        ax.plot(filtered_df['연도'], filtered_df['최고기온(℃)'], color='hotpink', marker='o', label='Max Temp')
        ax.plot(filtered_df['연도'], filtered_df['최저기온(℃)'], color='skyblue', marker='o', label='Min Temp')
        
        # 차트 세부 설정 (한글 깨짐을 방지하기 위해 라벨은 영문 및 기호 위주 표기)
        ax.set_title(f"Temperature Trend on {selected_month}/{selected_day} (1907-2018)", fontsize=14, pad=15)
        ax.set_xlabel("Year (연도)", fontsize=11)
        ax.set_ylabel("Temperature (℃)", fontsize=11)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='best')
        
        # 스트림릿에 그래프 출력
        st.pyplot(fig)
        
        # 6. 통계 정보 및 데이터 테이블 보기
        st.markdown("### 🔍 주요 기록")
        col1, col2 = st.columns(2)
        
        max_idx = filtered_df['최고기온(℃)'].idxmax()
        min_idx = filtered_df['최저기온(℃)'].idxmin()
        
        with col1:
            st.metric(
                label="역대 최고 기온", 
                value=f"{filtered_df.loc[max_idx, '최고기온(℃)']} ℃", 
                delta=f"{filtered_df.loc[max_idx, '연도']}년"
            )
        with col2:
            st.metric(
                label="역대 최저 기온", 
                value=f"{filtered_df.loc[min_idx, '최저기온(℃)']} ℃", 
                delta=f"{filtered_df.loc[min_idx, '연도']}년"
            )

        with st.expander("👉 전체 데이터 테이블 보기"):
            st.dataframe(filtered_df[['연도', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].reset_index(drop=True))

except FileNotFoundError:
    st.error("📂 디렉토리에서 `seoul.csv` 파일을 찾을 수 없습니다. 대시보드 앱 소스 파일과 같은 위치에 데이터를 업로드해 주세요.")
