import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 관광지 TOP10",
    layout="wide"
)

st.title("🌏 외국인 인기 서울 관광지 TOP10")

spots = [
    {
        "name": "경복궁",
        "lat": 37.579617,
        "lon": 126.977041,
        "subway": "경복궁역(3호선)",
        "fun": "한복체험 · 궁궐산책 · 야간관람"
    },
    {
        "name": "명동",
        "lat": 37.563757,
        "lon": 126.985302,
        "subway": "명동역(4호선)",
        "fun": "K뷰티쇼핑 · 길거리음식 · 야시장"
    },
    {
        "name": "홍대거리",
        "lat": 37.556350,
        "lon": 126.922672,
        "subway": "홍대입구역(2호선)",
        "fun": "버스킹 · 클럽 · 감성카페"
    },
    {
        "name": "N서울타워",
        "lat": 37.551169,
        "lon": 126.988227,
        "subway": "명동역(4호선)",
        "fun": "서울야경 · 케이블카 · 전망대"
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.582604,
        "lon": 126.983998,
        "subway": "안국역(3호선)",
        "fun": "한옥골목 · 전통카페 · 사진촬영"
    },
    {
        "name": "강남",
        "lat": 37.497942,
        "lon": 127.027621,
        "subway": "강남역(2호선)",
        "fun": "쇼핑 · 맛집 · 코엑스"
    },
    {
        "name": "롯데월드타워",
        "lat": 37.512568,
        "lon": 127.102535,
        "subway": "잠실역(2호선)",
        "fun": "서울스카이 · 쇼핑몰 · 아쿠아리움"
    },
    {
        "name": "DDP",
        "lat": 37.566526,
        "lon": 127.009224,
        "subway": "동대문역사문화공원역",
        "fun": "야경 · 디자인전시 · 야시장"
    },
    {
        "name": "익선동",
        "lat": 37.574369,
        "lon": 126.989451,
        "subway": "종로3가역",
        "fun": "한옥카페 · 감성맛집 · 사진명소"
    },
    {
        "name": "코엑스",
        "lat": 37.511820,
        "lon": 127.059159,
        "subway": "삼성역(2호선)",
        "fun": "별마당도서관 · 쇼핑 · 전시회"
    }
]

# 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11
)

marker_cluster = MarkerCluster().add_to(m)

# 마커 생성
for spot in spots:

    popup_html = f"""
    <b>{spot['name']}</b><br>
    클릭 후 아래 설명 확인
    """

    folium.Marker(
        [spot["lat"], spot["lon"]],
        popup=popup_html,
        tooltip=spot["name"],
        icon=folium.Icon(color="blue")
    ).add_to(marker_cluster)

# 지도 출력
map_data = st_folium(
    m,
    width=1200,
    height=600
)

st.divider()

# 클릭 이벤트
if map_data and map_data.get("last_clicked"):

    clicked_lat = map_data["last_clicked"]["lat"]
    clicked_lng = map_data["last_clicked"]["lng"]

    selected = None

    for spot in spots:
        if (
            abs(clicked_lat - spot["lat"]) < 0.01 and
            abs(clicked_lng - spot["lon"]) < 0.01
        ):
            selected = spot
            break

    if selected:
        st.subheader(f"📍 {selected['name']}")

        st.success(
            f"🚇 가까운 지하철역: {selected['subway']} | 🎉 놀거리: {selected['fun']}"
        )

else:
    st.info("지도의 관광지를 클릭해보세요.")
