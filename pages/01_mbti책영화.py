import streamlit as st

# --- 1. 데이터 구성 (1900년대 ~ 2010년대 대표작) ---
mbti_recommendations = {
    "ISTJ": {
        "book": {"title": "백년의 고독 (1967)", "author": "가브리엘 가르시아 마르케스", "desc": "철저한 연대기와 질서를 중시하는 ISTJ에게 추천하는 역사적 대서사시."},
        "movie": {"title": "명량 (2014)", "year": "2014", "cast": "최민식, 류승룡", "audience": "1,761만 명", "desc": "책임감과 원칙의 아이콘 이순신 장군의 고뇌를 그린 영화."}
    },
    "ISFJ": {
        "book": {"title": "어린 왕자 (1943)", "author": "생텍쥐페리", "desc": "소중한 관계를 지키려는 ISFJ의 따뜻한 마음과 어울리는 고전."},
        "movie": {"title": "국제시장 (2014)", "year": "2014", "cast": "황정민, 김윤진", "audience": "1,426만 명", "desc": "가족을 위해 평생을 헌신한 가장의 이야기."}
    },
    "INFJ": {
        "book": {"title": "데미안 (1919)", "author": "헤르만 헤세", "desc": "내면의 성찰과 자아를 찾는 INFJ에게 깊은 울림을 주는 책."},
        "movie": {"title": "기생충 (2019)", "year": "2019", "cast": "송강호, 이선균", "audience": "1,031만 명", "desc": "사회 구조와 인간 내면의 모순을 통찰력 있게 그려낸 걸작."}
    },
    "INTJ": {
        "book": {"title": "1984 (1949)", "author": "조지 오웰", "desc": "시스템의 모순을 분석하고 전략적으로 사고하는 INTJ를 위한 필독서."},
        "movie": {"title": "인셉션 (2010)", "year": "2010", "cast": "레오나르도 디카프리오", "audience": "599만 명", "desc": "복잡한 구조와 지적 유희를 즐기는 INTJ에게 최적화된 영화."}
    },
    "ISTP": {
        "book": {"title": "노인과 바다 (1952)", "author": "어네스트 헤밍웨이", "desc": "말보다는 행동, 묵묵히 자신의 일을 해내는 ISTP의 기질과 닮은 소설."},
        "movie": {"title": "범죄도시 (2017)", "year": "2017", "cast": "마동석, 윤계상", "audience": "688만 명", "desc": "군더더기 없는 액션과 효율적인 문제 해결력을 보여주는 영화."}
    },
    "ISFP": {
        "book": {"title": "호밀밭의 파수꾼 (1951)", "author": "J.D. 샐린저", "desc": "자유로운 영혼과 섬세한 감수성을 지닌 ISFP를 위한 이야기."},
        "movie": {"title": "건축학개론 (2012)", "year": "2012", "cast": "엄태웅, 한가인, 수지", "audience": "411만 명", "desc": "첫사랑의 아련한 감성과 시각적 영상미가 돋보이는 작품."}
    },
    "INFP": {
        "book": {"title": "상실의 시대 (1987)", "author": "무라카미 하루키", "desc": "고독과 사랑, 자아의 방황을 섬세하게 그린 INFP 맞춤형 소설."},
        "movie": {"title": "이터널 선샤인 (2004)", "year": "2004", "cast": "짐 캐리, 케이트 윈슬렛", "audience": "50만 명 (재개봉 포함)", "desc": "상상력 풍부한 연출과 깊은 감정선을 가진 INFP 인생 영화."}
    },
    "INTP": {
        "book": {"title": "멋진 신세계 (1932)", "author": "올더스 헉슬리", "desc": "지적 호기심과 비판적 사고를 즐기는 INTP를 위한 SF 고전."},
        "movie": {"title": "인터스텔라 (2014)", "year": "2014", "cast": "매튜 맥커너히, 앤 해서웨이", "audience": "1,032만 명", "desc": "과학적 상상력과 우주의 신비를 탐구하는 INTP의 지적 유희."}
    },
    "ESTP": {
        "book": {"title": "위대한 개츠비 (1925)", "author": "F. 스콧 피츠제럴드", "desc": "화려한 삶과 모험, 현재를 즐기는 ESTP에게 추천하는 소설."},
        "movie": {"title": "도둑들 (2012)", "year": "2012", "cast": "김윤석, 김혜수, 이정재", "audience": "1,298만 명", "desc": "박진감 넘치는 액션과 스릴을 즐기는 ESTP를 위한 영화."}
    },
    "ESFP": {
        "book": {"title": "바람과 함께 사라지다 (1936)", "author": "마거릿 미첼", "desc": "에너지 넘치고 열정적인 ESFP를 닮은 스칼렛 오하라의 이야기."},
        "movie": {"title": "써니 (2011)", "year": "2011", "cast": "유호정, 심은경", "audience": "736만 명", "desc": "함께 즐기는 에너지와 추억의 소중함을 아는 ESFP를 위한 영화."}
    },
    "ENFP": {
        "book": {"title": "빨강 머리 앤 (1908)", "author": "루시 모드 몽고메리", "desc": "무한한 상상력과 긍정 에너지를 가진 ENFP의 바이블."},
        "movie": {"title": "어바웃 타임 (2013)", "year": "2013", "cast": "도널 글리슨, 레이첼 맥아담스", "audience": "344만 명", "desc": "매 순간의 소중함과 사랑을 전하는 ENFP 맞춤 감성 영화."}
    },
    "ENTP": {
        "book": {"title": "돈키호테 (1605/근대소설의 효시)", "author": "미겔 데 세르반테스", "desc": "기존의 틀을 깨고 새로운 도전을 멈추지 않는 ENTP의 자화상."},
        "movie": {"title": "조커 (2019)", "year": "2019", "cast": "호아킨 피닉스", "audience": "525만 명", "desc": "사회적 관습에 질문을 던지고 혼돈 속의 본질을 꿰뚫는 ENTP를 위한 영화."}
    },
    "ESTJ": {
        "book": {"title": "자기경영노트 (1966)", "author": "피터 드러커", "desc": "효율성과 성과, 조직 관리에 탁월한 ESTJ를 위한 실용 지침서."},
        "movie": {"title": "베테랑 (2015)", "year": "2015", "cast": "황정민, 유아인", "audience": "1,341만 명", "desc": "추진력 있게 정의를 구현하는 주인공이 ESTJ의 쾌감을 자극함."}
    },
    "ESFJ": {
        "book": {"title": "작은 아씨들 (1868)", "author": "루이자 메이 올콧", "desc": "공동체의 화합과 따뜻한 유대감을 중시하는 ESFJ를 위한 고전."},
        "movie": {"title": "극한직업 (2019)", "year": "2019", "cast": "류승룡, 이하늬", "audience": "1,626만 명", "desc": "팀워크와 유쾌한 분위기 속에서 조화를 찾는 ESFJ를 위한 코미디."}
    },
    "ENFJ": {
        "book": {"title": "인간실격 (1948)", "author": "다자이 오사무", "desc": "타인의 감정에 공감하고 사회적 가면 속 진실을 고민하는 ENFJ를 위한 책."},
        "movie": {"title": "변호인 (2013)", "year": "2013", "cast": "송강호, 김영애", "audience": "1,137만 명", "desc": "신념을 위해 사람들을 이끄는 리더십과 공감 능력을 보여주는 영화."}
    },
    "ENTJ": {
        "book": {"title": "군주론 (1532/정치학의 고전)", "author": "니콜로 마키아벨리", "desc": "비전과 권력, 목표 달성을 위한 전략적 사고를 즐기는 ENTJ의 필독서."},
        "movie": {"title": "남산의 부장들 (2020)", "year": "2020", "cast": "이병헌, 이성민", "audience": "475만 명", "desc": "권력의 중심에서 전략적 선택과 결과를 치열하게 그리는 영화."}
    }
}

# --- 2. Streamlit UI 구성 ---
st.set_page_config(page_title="MBTI 시대별 추천", page_icon="📚")

st.title("✨ MBTI별 도서 & 영화 추천")
st.write("1900년대부터 2010년대까지의 명작 중에서 당신의 성향에 맞는 작품을 추천해 드립니다.")

# MBTI 선택
mbti_list = sorted(list(mbti_recommendations.keys()))
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", mbti_list)

if selected_mbti:
    rec = mbti_recommendations[selected_mbti]
    
    st.divider()
    
    # 도서 추천
    st.subheader(f"📖 {selected_mbti}를 위한 추천 도서")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.info("**제목/저자**")
    with col2:
        st.write(f"{rec['book']['title']} - {rec['book']['author']}")
    st.caption(f"💡 {rec['book']['desc']}")
    
    st.write("")
    
    # 영화 추천
    st.subheader(f"🎬 {selected_mbti}를 위한 추천 영화")
    
    # 표 형태로 정보 제공
    movie_info = {
        "항목": ["개봉 연도", "출연진", "관객 수 (한국 기준)"],
        "내용": [rec['movie']['year'], rec['movie']['cast'], rec['movie']['audience']]
    }
    st.table(movie_info)
    
    st.write(f"**영화 제목:** {rec['movie']['title']}")
    st.write(f"**설명:** {rec['movie']['desc']}")

st.sidebar.markdown("---")
st.sidebar.write("💡 **Tip**: Streamlit Cloud에서 바로 작동하는 코드입니다.")
