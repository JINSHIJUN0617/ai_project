import streamlit as st
import pandas as pd
import plotly.express as px
from collections import defaultdict

st.set_page_config(
    page_title="Pokemon Pokedex",
    page_icon="⚡",
    layout="wide"
)

# =========================
# 데이터 로드
# =========================

@st.cache_data
def load_data():
    return pd.read_csv("pokemon.csv")

df = load_data()

# =========================
# 타입 상성표
# =========================

TYPE_CHART = {
    "Normal": {"weak": ["Fighting"], "immune": ["Ghost"]},
    "Fire": {"weak": ["Water","Ground","Rock"], "resist": ["Fire","Grass","Ice","Bug","Steel","Fairy"]},
    "Water": {"weak": ["Electric","Grass"], "resist": ["Fire","Water","Ice","Steel"]},
    "Electric": {"weak": ["Ground"], "resist": ["Electric","Flying","Steel"]},
    "Grass": {"weak": ["Fire","Ice","Poison","Flying","Bug"], "resist": ["Water","Electric","Grass","Ground"]},
    "Ice": {"weak": ["Fire","Fighting","Rock","Steel"], "resist": ["Ice"]},
    "Fighting": {"weak": ["Flying","Psychic","Fairy"], "resist": ["Bug","Rock","Dark"]},
    "Poison": {"weak": ["Ground","Psychic"], "resist": ["Grass","Fighting","Poison","Bug","Fairy"]},
    "Ground": {"weak": ["Water","Grass","Ice"], "resist": ["Poison","Rock"], "immune": ["Electric"]},
    "Flying": {"weak": ["Electric","Ice","Rock"], "resist": ["Grass","Fighting","Bug"], "immune": ["Ground"]},
    "Psychic": {"weak": ["Bug","Ghost","Dark"], "resist": ["Fighting","Psychic"]},
    "Bug": {"weak": ["Fire","Flying","Rock"], "resist": ["Grass","Fighting","Ground"]},
    "Rock": {"weak": ["Water","Grass","Fighting","Ground","Steel"], "resist": ["Normal","Fire","Poison","Flying"]},
    "Ghost": {"weak": ["Ghost","Dark"], "resist": ["Poison","Bug"], "immune": ["Normal","Fighting"]},
    "Dragon": {"weak": ["Ice","Dragon","Fairy"], "resist": ["Fire","Water","Electric","Grass"]},
    "Dark": {"weak": ["Fighting","Bug","Fairy"], "resist": ["Ghost","Dark"], "immune": ["Psychic"]},
    "Steel": {"weak": ["Fire","Fighting","Ground"], "resist": ["Normal","Grass","Ice","Flying","Psychic","Bug","Rock","Dragon","Steel","Fairy"], "immune": ["Poison"]},
    "Fairy": {"weak": ["Poison","Steel"], "resist": ["Fighting","Bug","Dark"], "immune": ["Dragon"]}
}

ALL_TYPES = list(TYPE_CHART.keys())

# =========================
# 상성 계산 함수
# =========================

def calculate_type_matchup(type1, type2=None):

    multiplier = defaultdict(lambda: 1)

    for defend_type in [type1, type2]:

        if pd.isna(defend_type):
            continue

        if defend_type not in TYPE_CHART:
            continue

        info = TYPE_CHART[defend_type]

        for t in info.get("weak", []):
            multiplier[t] *= 2

        for t in info.get("resist", []):
            multiplier[t] *= 0.5

        for t in info.get("immune", []):
            multiplier[t] *= 0

    weakness_4 = []
    weakness_2 = []
    resist_half = []
    resist_quarter = []
    immune = []

    for t in ALL_TYPES:

        value = multiplier[t]

        if value == 4:
            weakness_4.append(t)

        elif value == 2:
            weakness_2.append(t)

        elif value == 0.5:
            resist_half.append(t)

        elif value == 0.25:
            resist_quarter.append(t)

        elif value == 0:
            immune.append(t)

    return weakness_4, weakness_2, resist_half, resist_quarter, immune


# =========================
# 사이드바
# =========================

st.sidebar.title("포켓몬 필터")

search = st.sidebar.text_input("검색")

# 타입 필터
all_types_df = sorted(
    pd.concat([df["TYPE1"], df["TYPE2"]])
    .dropna()
    .unique()
)

selected_type = st.sidebar.selectbox(
    "타입",
    ["전체"] + list(all_types_df)
)

# 세대 필터
gens = sorted(df["GENERATION"].dropna().unique())

selected_gen = st.sidebar.selectbox(
    "세대",
    ["전체"] + list(gens)
)

# 전설 필터
legendary_filter = st.sidebar.selectbox(
    "전설 여부",
    ["전체", "전설만", "일반만"]
)

# =========================
# 필터링
# =========================

filtered = df.copy()

if search:
    filtered = filtered[
        filtered["NAME"]
        .astype(str)
        .str.contains(search, case=False)
    ]

if selected_type != "전체":
    filtered = filtered[
        (filtered["TYPE1"] == selected_type)
        |
        (filtered["TYPE2"] == selected_type)
    ]

if selected_gen != "전체":
    filtered = filtered[
        filtered["GENERATION"] == selected_gen
    ]

if "LEGENDARY" in filtered.columns:

    if legendary_filter == "전설만":
        filtered = filtered[
            filtered["LEGENDARY"] == True
        ]

    elif legendary_filter == "일반만":
        filtered = filtered[
            filtered["LEGENDARY"] == False
        ]

# =========================
# 메인
# =========================

st.title("⚡ 포켓몬 도감")

if len(filtered) == 0:
    st.warning("검색 결과 없음")
    st.stop()

pokemon_name = st.selectbox(
    "포켓몬 선택",
    filtered["NAME"].unique()
)

pokemon = filtered[
    filtered["NAME"] == pokemon_name
].iloc[0]

# =========================
# 이미지
# =========================

col1, col2 = st.columns([1,2])

with col1:

    try:

        dex = int(pokemon["NUMBER"])

        image_url = (
            "https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/"
            f"sprites/pokemon/other/official-artwork/{dex}.png"
        )

        st.image(image_url)

    except:
        st.info("이미지 없음")

with col2:

    st.header(pokemon["NAME"])

    if "FORM" in pokemon.index:
        st.write("폼:", pokemon["FORM"])

    st.write(
        "타입:",
        pokemon["TYPE1"],
        f"/ {pokemon['TYPE2']}" if pd.notna(pokemon["TYPE2"]) else ""
    )

    if "CATEGORY" in pokemon.index:
        st.write("분류:", pokemon["CATEGORY"])

    if "GENERATION" in pokemon.index:
        st.write("세대:", pokemon["GENERATION"])

    if "HEIGHT" in pokemon.index:
        st.write("키:", pokemon["HEIGHT"], "m")

    if "WEIGHT" in pokemon.index:
        st.write("몸무게:", pokemon["WEIGHT"], "kg")

# =========================
# 능력치
# =========================

st.subheader("종족값")

stats_df = pd.DataFrame({
    "Stat":[
        "HP",
        "ATK",
        "DEF",
        "SP ATK",
        "SP DEF",
        "SPD"
    ],
    "Value":[
        pokemon["HP"],
        pokemon["ATK"],
        pokemon["DEF"],
        pokemon["SP ATK"],
        pokemon["SP DEF"],
        pokemon["SPD"]
    ]
})

fig = px.line_polar(
    stats_df,
    r="Value",
    theta="Stat",
    line_close=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.metric(
    "종족값 총합",
    int(pokemon["TOTAL"])
)

# =========================
# 순위
# =========================

rank = (
    df["TOTAL"]
    .rank(
        ascending=False,
        method="min"
    )
)

my_rank = int(rank[pokemon.name])

st.metric(
    "전체 종족값 순위",
    f"{my_rank}위"
)

# =========================
# 타입 상성
# =========================

st.subheader("타입 상성")

weak4, weak2, resist, resist25, immune = calculate_type_matchup(
    pokemon["TYPE1"],
    pokemon["TYPE2"]
)

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.error("4배 약점")
    st.write(", ".join(weak4) if weak4 else "-")

with c2:
    st.warning("2배 약점")
    st.write(", ".join(weak2) if weak2 else "-")

with c3:
    st.success("반감")
    st.write(", ".join(resist) if resist else "-")

with c4:
    st.success("1/4 반감")
    st.write(", ".join(resist25) if resist25 else "-")

with c5:
    st.info("무효")
    st.write(", ".join(immune) if immune else "-")

# =========================
# 카운터 추천
# =========================

st.subheader("추천 카운터 포켓몬")

counter_types = weak4 + weak2

counter_df = df[
    (df["TYPE1"].isin(counter_types))
    |
    (df["TYPE2"].isin(counter_types))
]

counter_df = (
    counter_df
    .sort_values(
        "TOTAL",
        ascending=False
    )
    .drop_duplicates("NAME")
    .head(3)
)

for _, row in counter_df.iterrows():
    st.write(
        f"🏆 {row['NAME']} (종족값 {row['TOTAL']})"
    )

# =========================
# 비슷한 타입 추천
# =========================

st.subheader("비슷한 타입 포켓몬")

similar = df[
    (df["TYPE1"] == pokemon["TYPE1"])
    |
    (df["TYPE2"] == pokemon["TYPE1"])
]

similar = (
    similar
    .drop_duplicates("NAME")
    .head(5)
)

for _, row in similar.iterrows():
    st.write(row["NAME"])

# =========================
# 포켓몬GO 참고 점수
# =========================

go_score = (
    pokemon["ATK"] * 2
    + pokemon["DEF"]
    + pokemon["HP"]
)

st.subheader("Pokémon GO 참고")

st.metric(
    "예상 GO 점수",
    int(go_score)
)

# =========================
# 데이터 테이블
# =========================

st.subheader("전체 데이터")

st.dataframe(
    filtered,
    use_container_width=True
)
