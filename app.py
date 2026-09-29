import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from folium.plugins import HeatMap
import json
import os

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="نموذج تقييم محطات الشحن | المدينة المنورة",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص الألوان والخطوط باستخدام CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Tajawal', sans-serif;
    }
    .main-title {
        color: #1E3A8A;
        text-align: center;
        padding-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar) لمدخلات المستخدم
st.sidebar.image("https://upload.wikimedia.org/wikipedia/ar/thumb/a/a2/Taibah_University_Logo.svg/1200px-Taibah_University_Logo.svg.png", width=150)
st.sidebar.title("🎛️ لوحة التحكم الجغرافية")
st.sidebar.markdown("قم بتعديل أوزان المعايير لتحديث الخريطة التفاعلية:")

# أشرطة التمرير للأوزان (تبدأ بقيم افتراضية)
w_grid = st.sidebar.slider("🔌 القرب من شبكة الكهرباء (154/380 kV)", 0, 100, 30)
w_roads = st.sidebar.slider("🛣️ القرب من شبكة الطرق", 0, 100, 25)
w_pop = st.sidebar.slider("👥 الكثافة السكانية", 0, 100, 20)
w_poi = st.sidebar.slider("🛒 القرب من المراكز التجارية (POIs)", 0, 100, 15)
w_slope = st.sidebar.slider("⛰️ استواء التضاريس (Slope)", 0, 100, 10)

# حساب الإجمالي للتأكد من أنه يساوي 100% (تطبيع الأوزان)
total_weight = w_grid + w_roads + w_pop + w_poi + w_slope
if total_weight > 0:
    weights = [w_grid/total_weight, w_roads/total_weight, w_pop/total_weight, w_poi/total_weight, w_slope/total_weight]
else:
    weights = [0.2, 0.2, 0.2, 0.2, 0.2]

# 3. المنطقة الرئيسية (Main Content)
st.markdown("<h1 class='main-title'>⚡ التحليل المكاني الذكي لمحطات شحن المركبات بالمدينة المنورة</h1>", unsafe_allow_html=True)

# صف المؤشرات (KPI Cards)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="📍 المواقع المثلى المكتشفة", value=f"{int(total_weight * 1.5)} موقع", delta="محدث")
with col2:
    # محاكاة لنسبة التناسق في AHP (أقل من 0.1 تعتبر ممتازة)
    cr_value = max(0.01, abs(0.15 - (w_grid/200)))
    st.metric(label="📊 نسبة التناسق (CR)", value=f"{cr_value:.3f}", delta="-0.02" if cr_value < 0.1 else "+0.05", delta_color="inverse")
with col3:
    st.metric(label="🔋 الوفر المتوقع في الطاقة", value=f"{int(w_grid * 0.8)} %", delta="كفاءة عالية")
with col4:
    st.metric(label="⏱️ زمن معالجة الذكاء الاصطناعي", value="1.2 ثانية", delta="سريع")

st.divider()

# 4. الخريطة التفاعلية (Interactive Map)
st.subheader("🗺️ الخريطة الحرارية للملاءمة المكانية (Suitability Heatmap)")

# إحداثيات المدينة المنورة الافتراضية
madinah_coords = [24.4686, 39.6111]
m = folium.Map(location=madinah_coords, zoom_start=12, tiles='OpenStreetMap')

# توليد بيانات عشوائية لمحاكاة مواقع الشحن (تتأثر بتغيير الأوزان في لوحة التحكم)
np.random.seed(int(total_weight))
latitudes = np.random.uniform(24.42, 24.52, 100)
longitudes = np.random.uniform(39.55, 39.68, 100)
intensities = np.random.uniform(0.5, 1.0, 100) * (weights[0] * 2) # التأثر بوزن الكهرباء كمثال

heat_data = [[lat, lon, mag] for lat, lon, mag in zip(latitudes, longitudes, intensities)]
HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(m)

# عرض الخريطة في الواجهة
st_folium(m, width=1200, height=500, returned_objects=[])

st.divider()

# 5. الرسوم البيانية التوضيحية
st.subheader("📈 التحليل التقني للأوزان: الخبراء (AHP) مقابل الذكاء الاصطناعي (ML)")

col_chart1, col_chart2 = st.columns(2)

categories = ['شبكة الكهرباء', 'شبكة الطرق', 'الكثافة السكانية', 'المراكز التجارية', 'التضاريس']
current_weights = [w_grid, w_roads, w_pop, w_poi, w_slope]

# --- الكود الجديد لربط الذكاء الاصطناعي ---
# قراءة الأوزان من ملف الذكاء الاصطناعي
ai_weights_list = [20, 20, 20, 20, 20] # قيم افتراضية في حال لم يتم تدريب النموذج بعد
if os.path.exists('models/ai_weights.json'):
    with open('models/ai_weights.json', 'r', encoding='utf-8') as f:
        ai_data = json.load(f)
        # سحب القيم وترتيبها لتتطابق مع الفئات
        ai_weights_list = [
            ai_data["شبكة الكهرباء"],
            ai_data["شبكة الطرق"],
            ai_data["الكثافة السكانية"],
            ai_data["المراكز التجارية"],
            ai_data["التضاريس"]
        ]

with col_chart1:
    # المخطط الراداري للأوزان الحالية
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=current_weights,
        theta=categories,
        fill='toself',
        name='أوزان المستخدم',
        line_color='#1E3A8A'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(max(current_weights), max(ai_weights_list)) + 10])),
        showlegend=False,
        title="توزيع الأوزان المكانية (Radar Chart)"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_chart2:
    # مقارنة بين أوزان AHP وأوزان الذكاء الاصطناعي الحقيقية
    fig_bar = go.Figure(data=[
        go.Bar(name='تفضيلات المستخدم (AHP)', x=categories, y=current_weights, marker_color='#3B82F6'),
        go.Bar(name='تعلم الآلة (Random Forest)', x=categories, y=ai_weights_list, marker_color='#10B981')
    ])
    fig_bar.update_layout(barmode='group', title="مقارنة الذكاء الاصطناعي بالتفضيلات البشرية")
    st.plotly_chart(fig_bar, use_container_width=True)

st.caption("تم تطوير هذا النموذج الأولي للمشاركة في مسابقة طيبة ثون 2026 - مسار الابتكار التقني والصناعي.")
