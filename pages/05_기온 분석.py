import streamlit as st
import pandas as pd

# 1. 페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="서울 기온 역사 데이터 분석", layout="centered")
st.title("📅 서울 연도별 특정 날짜 기온 추이 분석")
st.write("1907년부터 2018년까지, 선택하신 날짜의 최고/최저 기온 변화를 확인해보세요.")

# 2. 데이터 로드 및 전처리 (UnicodeDecodeError 대응 완료)
@st.cache_data
def load_data():
    paths = ["seoul.csv", "../seoul.csv"] # 메인 앱 위치에 따른 경로 후보들
    df = None
    
    # 여러 경로와 여러 인코딩(cp949, utf-8) 조합을 시도하여 안전하게 파일을 읽어옵니다.
    for path in paths:
        try:
            # 1순위: 한글 완성형 인코딩인 cp949로 시도
            df = pd.read_csv(path, encoding='cp949')
            break
        except (FileNotFoundError, UnicodeDecodeError):
            try:
                # 2순위: 혹시 모를 utf-8 인코딩으로 재시도
                df = pd.read_csv(path, encoding='utf-8')
                break
            except (FileNotFoundError, UnicodeDecodeError):
                continue
                
    if df is None:
        raise FileNotFoundError("seoul.csv 파일을 찾을 수 없거나 파일의 인코딩을 지원하지 않습니다.")
        
    # 컬럼명 공백 제거 및 날짜 데이터 전처리 (\t 제거)
    df.columns = df.columns.str.strip()
    df['날짜'] = df['날짜'].astype(str).str.replace('\t', '').str.strip()
    
    # 결측치 제거
    df = df.dropna(subset=['최고기온(℃)', '최저기온(℃)'])
    
    # 날짜 데이터 타입을 datetime으로 변경 후 연, 월, 일 분리
    df['날짜_dt'] = pd.to_datetime(df['날짜'], errors='coerce')
    df = df.dropna(subset=['날짜_dt'])
    
    df['연도'] = df['날짜_dt'].dt.year
    df['월'] = df['날짜_dt'].dt.month
    df['일'] = df['날짜_dt'].dt.day
    
    return df

try:
    df = load_data()

    # 3. 사이드바 - 월/일 선택 UI 구현
    st.sidebar.header("📅 날짜 선택")
    selected_month = st.sidebar.selectbox("월을 선택하세요", list(range(1, 13)), index=9) # 기본값 10월
    
    available_days = sorted(df[df['월'] == selected_month]['일'].unique())
    selected_day = st.sidebar.selectbox("일을 선택하세요", available_days, index=0)

    # 4. 데이터 필터링
    filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

    if filtered_df.empty:
        st.warning("선택하신 날짜에 해당하는 데이터가 없습니다.")
    else:
        st.subheader(f"📊 {selected_month}월 {selected_day}일의 연도별 기온 변화")
        
        # 5. 스트림릿 내장 차트용 데이터 가공 (X축을 연도로 설정)
        chart_data = filtered_df.set_index('연도')[['최고기온(℃)', '최저기온(℃)']]
        chart_data.columns = ['Max Temp', 'Min Temp']
        
        # 6. 스트림릿 기본 line_chart 사용 (색상 지정: 최고=핫핑크, 최저=연한 파란색)
        st.line_chart(
            chart_data, 
            color=["#FF69B4", "#87CEEB"]
        )
        
        # 7. 통계 정보 및 데이터 테이블 보기
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

except Exception as e:
    st.error(f"⚠️ 에러가 발생했습니다: {e}")
    st.info("데이터 파일(seoul.csv)이 올바른 위치에 있는지, 파일 형식이 올바른지 확인해 주세요.")
