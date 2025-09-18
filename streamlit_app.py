# streamlit_app.py

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# ----------------------------
# 페이지 기본 설정
# ----------------------------
st.set_page_config(page_title="바다가 끓으면 교실도 끓는다", layout="wide")

# ----------------------------
# 서론
# ----------------------------
st.title("🌊 바다가 끓으면 교실도 끓는다")
st.subheader("해수온 상승이 폭염과 청소년 학습 환경에 미치는 연쇄 영향 분석")

st.markdown("""
> 기후위기는 이미 교실 안까지 들어왔습니다.  
> **바다의 온도 상승**은 단지 해양 생태계만의 문제가 아니라,  
> **폭염을 심화**시키고 결국 **청소년의 건강, 집중력, 학습권**을 위협하고 있어요.
""")

# ----------------------------
# 해수온 상승 데이터 시각화
# ----------------------------
st.header("📈 해수온 상승과 폭염의 연관성")

years = list(range(1989, 2023))
avg_deviation = [
    -6.2, -4.8, -3.3, -2.5, -1.0, 0.1, 0.2, 0.5, 1.1, 0.3,
    0.9, 1.5, 1.6, 1.4, 2.0, 1.8, 2.3, 2.5, 3.1, 3.0,
    3.5, 4.2, 4.8, 5.1, 6.2, 6.8, 7.4, 8.1, 9.1, 10.3,
    10.6, 11.1, 11.8, 12.5
]
df = pd.DataFrame({"연도": years, "해수면 편차(cm)": avg_deviation})

fig = px.line(df, x="연도", y="해수면 편차(cm)",
              title="📊 연평균 해수면 높이 편차 (1989~2022)",
              markers=True)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
- **평균 상승률**: +3.03mm/yr  
- **상승 추세**는 점점 **가팔라지고 있음**
""")

# ----------------------------
# 폭염과 학습 환경
# ----------------------------
st.header("🔥 폭염은 교실을 데운다")

st.markdown("""
### 🔹 폭염과 학습 집중력

- 기온 1도 상승 → **집중력 10% 감소**  
- 폭염 시 **학업 성취도 평균 15% 하락**
- 실내 온도 28도 초과 시, **인지 능력 저하** 급격히 증가

> 💬 *"폭염 날씨에는 쉬는 시간 후 교실에 들어가는 것만으로도 숨이 막혀요"* – 고등학생 인터뷰
""")

# ----------------------------
# 에어컨 사용 시뮬레이션
# ----------------------------
st.header("💨 에어컨의 역설")

st.markdown("가정용 에어컨 **1대**는 1시간 가동 시 약 **0.8kWh**의 전력을 소비합니다.")

col1, col2 = st.columns(2)
with col1:
    hours = st.slider("하루 평균 사용 시간 (시간)", 0, 24, 6)
with col2:
    days = st.slider("총 사용 일수 (일)", 1, 90, 30)

energy = hours * days * 0.8
co2 = round(energy * 0.424, 2)  # kg CO₂

st.markdown(f"""
#### 🧮 결과
- 🔌 총 전력 사용량: <span style='font-size:24px; color:orange; font-weight:bold'>{energy:.1f} kWh</span>  
- 🌍 CO₂ 배출량: <span style='font-size:24px; color:red; font-weight:bold'>{co2:.1f} kg</span>  
""", unsafe_allow_html=True)

st.caption("※ CO₂ 배출량 계산 기준: 한국 전력 평균 배출계수 0.424 kg/kWh")

# ----------------------------
# 해수면 1m 상승 지도 시뮬레이션
# ----------------------------
st.header("🌍 해수면 상승 시뮬레이션 지도")

st.markdown("해수면이 상승하면 **저지대 침수 위험 지역**이 바다색으로 표시됩니다. (파랑 → 빨강)")

sea_level_cm = st.slider("예상 해수면 상승(cm)", 0, 200, 100, step=10)

# 샘플 해안 지역 데이터
regions = [
    {"name": "부산", "lat": 35.18, "lon": 129.08, "base_risk": 120},
    {"name": "인천", "lat": 37.45, "lon": 126.70, "base_risk": 100},
    {"name": "제주", "lat": 33.50, "lon": 126.53, "base_risk": 80},
    {"name": "여수", "lat": 34.75, "lon": 127.66, "base_risk": 90},
    {"name": "서울", "lat": 37.56, "lon": 126.97, "base_risk": 50},
]

# 색상 매핑 함수
def risk_color(risk):
    if risk >= 200:
        return "darkred"
    elif risk >= 150:
        return "orangered"
    elif risk >= 100:
        return "orange"
    elif risk >= 50:
        return "lightblue"
    else:
        return "blue"

# 지도 생성
m = folium.Map(location=[36.2, 127.9], zoom_start=6)

for r in regions:
    total_risk = r["base_risk"] + sea_level_cm
    folium.CircleMarker(
        location=[r["lat"], r["lon"]],
        radius=18,
        popup=f"{r['name']} (위험도: {total_risk}cm)",
        color=risk_color(total_risk),
        fill=True,
        fill_color=risk_color(total_risk),
        fill_opacity=0.7
    ).add_to(m)

# 지도 범례 추가
legend_html = """
<div style='position: fixed; 
     bottom: 40px; left: 40px; width: 180px; height: 140px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; padding: 10px;'>
<b>🌊 위험도 색상 범례</b><br>
<span style='color:blue;'>●</span> 안전 (0~50cm)<br>
<span style='color:lightblue;'>●</span> 주의 (50~100cm)<br>
<span style='color:orange;'>●</span> 경고 (100~150cm)<br>
<span style='color:orangered;'>●</span> 위험 (150~200cm)<br>
<span style='color:darkred;'>●</span> 매우 위험 (200cm 이상)
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))
st_data = st_folium(m, width=800, height=500)

# ----------------------------
# 결론
# ----------------------------
st.header("📌 결론: 청소년이 바다와 교실을 함께 지키려면")

st.markdown("""
- **교실 온도 26도 유지 캠페인**
- **에어컨 최소화 & 선풍기 병행 사용**
- **불필요한 전기 소모 줄이기**
- **여름 방학 기간 기후교육 강화**

> 청소년의 작은 실천이 **몰디브 해안도 지키고**,  
> **우리 교실의 온도도 지킬 수 있습니다.**
""")

st.caption("📚 출처: 해양환경공단, 뉴스펭귄, 비즈니스포스트, 국립해양조사원, YTN Science")