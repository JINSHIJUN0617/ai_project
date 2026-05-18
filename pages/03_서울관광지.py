import streamlit as st
import folium
from streamlit.components.v1 import html

st.set_page_config(
    page_title="서울 관광지 TOP10",
    layout="wide"
)

st.title("🌏 외국인 인기 서울 관광지 TOP10")
st.write("관광지를 클릭하면 아래에 가까운 지하철역과 놀거리가 표시됩니다.")

# 관광지 데이터
spots = [
    {"name": "경복궁", "lat": 37.579617, "lon": 126.977041, "info": "🚇 경복궁역(3호선) | 🎉 한복체험 · 궁궐산책"},
    {"name": "명동", "lat": 37.563757, "lon": 126.985302, "info": "🚇 명동역(4호선) | 🎉 쇼핑 · 길거리음식"},
    {"name": "홍대거리", "lat": 37.556350, "lon": 126.922672, "info": "🚇 홍대입구역(2호선) | 🎉 버스킹 · 감성카페"},
    {"name": "N서울타워", "lat": 37.551169, "lon": 126.988227, "info": "🚇 명동역(4호선) | 🎉 서울야경 · 전망대"},
    {"name": "북촌한옥마을", "lat": 37.582604, "lon": 126.983998, "info": "🚇 안국역(3호선) | 🎉 한옥골목 · 전통카페"},
    {"name": "강남", "lat": 37.497942, "lon": 127.027621, "info": "🚇 강남역(2호선) | 🎉 쇼핑 · 맛집"},
    {"name": "롯데월드타워", "lat": 37.512568, "lon": 127.102535, "info": "🚇 잠실역(2호선) | 🎉 전망대 · 아쿠아리움"},
    {"name": "DDP", "lat": 37.566526, "lon": 127.009224, "info": "🚇 동대문역사문화공원역 | 🎉 야시장 · 전시"},
    {"name": "익선동", "lat": 37.574369, "lon": 126.989451, "info": "🚇 종로3가역 | 🎉 한옥카페 · 사진명소"},
    {"name": "코엑스", "lat": 37.511820, "lon": 127.059159, "info": "🚇 삼성역(2호선) | 🎉 별마당도서관 · 쇼핑"}
]

# Folium 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

# 마커 추가 (팝업은 이름만)
for spot in spots:
    folium.Marker(
        [spot["lat"], spot["lon"]],
        popup=spot["name"],  # 지도에서 클릭 시 이름만 보임
        tooltip=spot["name"],
        icon=folium.Icon(color="blue")
    ).add_to(m)

# 지도를 HTML로 변환
map_html = m._repr_html_()
html(map_html, height=700)

# 클릭 좌표 입력
st.write("---")
st.write("📌 관광지 선택")

clicked_name = st.selectbox(
    "아래 목록에서 관광지를 선택하세요 (지도 클릭 대신 선택 가능)",
    [""] + [spot["name"] for spot in spots]
)

if clicked_name:
    selected_spot = next(spot for spot in spots if spot["name"] == clicked_name)
    st.subheader(f"{selected_spot['name']}")
    st.success(selected_spot["info"])
