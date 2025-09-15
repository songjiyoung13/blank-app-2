import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="여름을 삼킨 바다", layout="wide")

# 1. 헤더
st.title("🌊 여름을 삼킨 바다")
st.subheader("에어컨 한 번 덜 켰다면, 몰디브는 가라앉지 않았을지도 몰라요")

st.markdown("""
기후위기, 특히 해수면 상승은 더 이상 먼 나라 이야기만이 아닙니다.  
에어컨 사용, 전기 낭비, 산업 활동은 우리 일상 속 기후 악화를 가속시키고 있어요.  
이 웹은 **해수면 상승 데이터**와 **청소년 일상 속 행동**을 연결하여,  
**여름휴양지와 삶에 어떤 영향을 미치는지** 보여줍니다.
""")

# 2. 시뮬레이터(요약)
st.header("🏖️ 해수면이 1m 오른다면, 어떤 일이 벌어질까요?")
st.image("https://cdn.newspenguin.com/news/photo/2020/05/27/14133_6944_3516.jpg", caption="KOEM 시뮬레이터 기반 가상 시나리오")

rise_cm = st.slider("예상 해수면 상승(cm)", 0, 200, 50, step=10)

if rise_cm >= 100:
    st.error("⚠️ 1m 이상 상승 시, **서울 일부 저지대** 포함 해안선 침수 가능")
elif rise_cm >= 50:
    st.warning("🌀 인천·부산 해안가 일부 지역 침수 위험")
else:
    st.success("✅ 해안 침수 위험은 상대적으로 낮지만 방심은 금물!")

st.caption("시뮬레이터 출처: 해양환경공단(KOEM) [rcp45 시나리오 기준]")

# 3. 실시간 해수면 상승 데이터 (예시 데이터)
st.header("📈 실제 해수면은 얼마나 올랐을까?")

# 예시 데이터 (실제 API나 CSV 대체 가능)
years = list(range(1993, 2024))
levels = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7,
          1.9, 2.1, 2.3, 2.6, 2.8, 3.1, 3.3, 3.6, 3.9, 4.2,
          4.5, 4.9, 5.3, 5.8, 6.3, 6.9, 7.5, 8.2, 9.0, 9.8, 10.7]

df = pd.DataFrame({"Year": years, "Sea Level (cm)": levels})
fig = px.line(df, x="Year", y="Sea Level (cm)", title="📊 글로벌 해수면 상승 추이 (1993~2023)")
st.plotly_chart(fig, use_container_width=True)

# 4. 에어컨 사용 시뮬레이션
st.header("💡 에어컨은 바다를 데운다?")

st.markdown("1대의 가정용 에어컨이 **1시간 가동 시 약 0.8kWh 전력**을 사용합니다.")
hours = st.slider("하루 평균 에어컨 사용 시간", 0, 24, 8)
days = st.slider("하루 수", 0, 90, 30)

energy = hours * days * 0.8
co2 = round(energy * 0.424, 2)  # kg CO2 배출 (한국 평균 배출계수)

st.write(f"🔌 총 전력 사용량: {energy:.1f} kWh")
st.write(f"🌍 예상 CO₂ 배출량: {co2:.1f} kg → 바다 수온에 간접 영향")

# 5. 기사 요약 카드
st.header("📰 기후위기 관련 뉴스 요약")

col1, col2 = st.columns(2)

with col1:
    st.image("https://www.businesspost.co.kr/news/photo/202312/20231219172630_40312.jpg", use_column_width=True)
    st.markdown("해수면 상승으로 인해 인기 관광지들이 실제로 가라앉고 있다는 경고가 속속 등장합니다.")
    st.markdown("[👉 원문보기](https://www.businesspost.co.kr)")
with col2:
    st.image("https://cdn.newspenguin.com/news/photo/2020/05/27/14133_6944_3516.jpg", use_column_width=True)
    st.markdown("**에어컨의 역습**")  
    st.markdown("여름철 필수품이 된 에어컨, 하지만 과도한 전력 사용은 지구 온난화의 주범 중 하나입니다.") 
    st.markdown("[👉 뉴스펭귄 보기](https://www.newspenguin.com/news/articleView.html?idxno=14133)")

# 6. 결론
st.header("📌 결론: 우리의 여름을 지키기 위해")

st.markdown("""
- 에어컨 온도는 1~2도 높이고, 사용시간을 줄여보세요.
- 사용하지 않는 공간은 반드시 에어컨을 꺼주세요.
- 실내에서도 선풍기·차양막 등 다양한 방법을 활용해요.

> 💬 나의 작은 변화가 몰디브, 제주도, 강릉의 해변을 지킬 수 있습니다.
""")

st.caption("자료 출처: 해양환경공단, Copernicus, 뉴스펭귄, 비즈니스포스트, NASA")
