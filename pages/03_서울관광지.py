import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(
    page_title="서울 외국인 인기 관광지 TOP10",
    layout="wide"
)

st.title("🌏 외국인들이 좋아하는 서울 관광지 TOP10")
st.markdown("관광지를 클릭하면 아래에 가까운 지하철역과 놀거리를 확인할 수 있습니다.")

# 서울 관광지 데이터
spots = [
    {
        "name": "경복궁",
        "lat": 37.579617,
        "lon": 126.977041,
        "subway": "경복궁역(3호선)",
        "fun": "한복 체험, 궁궐 산책, 국립민속박물관"
    },
    {
        "name": "명동",
        "lat": 37.563757,
        "lon": 126.985302,
        "subway": "명동역(4호선)",
        "fun": "K-뷰티 쇼핑, 길거리 음식, 야간 쇼핑"
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.582604,
        "lon": 126.983998,
        "subway": "안국역(3호선)",
        "fun": "전통 한옥 골목 산책, 카페 투어, 공예 체험"
    },
    {
        "name": "N서울타워",
        "lat": 37.551169,
        "lon": 126.988227,
        "subway": "명동역(4호선)",
        "fun": "서울 야경 감상, 케이블카, 사랑의 자물쇠"
    },
    {
        "name": "홍대거리",
        "lat": 37.556350,
        "lon": 126.922672,
        "subway": "홍대입구역(2호선)",
        "fun": "버스킹 공연, 클럽, 감성 카페"
    },
    {
        "name": "강남",
        "lat": 37.497942,
        "lon": 127.027621,
        "subway": "강남역(2호선)",
        "fun": "쇼핑, 맛집 탐방, 코엑스 방문"
    },
    {
        "name": "롯데월드타워",
        "lat": 37.512568,
        "lon": 127.102535,
        "subway": "잠실역(2호선)",
        "fun": "서울스카이 전망대, 쇼핑몰, 아쿠아리움"
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "lat": 37.566526,
        "lon": 127.009224,
        "subway": "동대문역사문화공원역(2·4·5호선)",
        "fun": "야경, 디자인 전시, 야시장"
    },
    {
        "name": "익선동",
        "lat": 37.574369,
        "lon": 126.989451,
        "subway": "종로3가역(1·3·5호선)",
        "fun": "한옥 카페, 맛집, 감성 사진 촬영"
    },
    {
        "name": "코엑스",
        "lat": 37.511820,
        "lon": 127.059159,
        "subway": "삼성역(2호선)",
        "fun": "별마당도서관, 쇼핑, 전시회"
    }
]

# 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11,
    tiles="CartoDB positron"
)

marker_cluster = MarkerCluster().add_to(m)

# 마커 추가
for idx, spot in enumerate(spots):
    popup_html = f"""
    <b>{spot['name']}</b><br>
    클릭 후 아래 설명 확인
    """

    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=spot["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(marker_cluster)

# 지도 출력
map_data = st_folium(
    m,
    width=1200,
    height=650,
    returned_objects=["last_object_clicked"]
)

st.divider()

# 클릭된 관광지 정보 출력
clicked = map_data.get("last_object_clicked")

if clicked:
    clicked_lat = clicked["lat"]
    clicked_lon = clicked["lng"]

    selected_spot = None

    for spot in spots:
        if (
            abs(spot["lat"] - clicked_lat) < 0.0001 and
            abs(spot["lon"] - clicked_lon) < 0.0001
        ):
            selected_spot = spot
            break

    if selected_spot:
        st.subheader(f"📍 {selected_spot['name']}")
        st.success(
            f"🚇 가까운 지하철역: {selected_spot['subway']} | 🎉 놀거리: {selected_spot['fun']}"
        )
else:
    st.info("지도에서 관광지를 클릭해보세요.")
