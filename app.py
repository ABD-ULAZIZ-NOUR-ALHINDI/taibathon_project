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

# تخصيص الألوان والخطوط ودمج تصميم البطاقات الحديث باستخدام CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Tajawal', sans-serif;
    }
    /* دعم اللغة العربية للواجهة */
    .stApp {
        direction: rtl;
    }
    .main-title {
        color: #1E3A8A;
        text-align: center;
        padding-bottom: 20px;
        font-weight: bold;
    }
    /* تصميم بطاقات الاستثمار */
    .pricing-card {
        background-color: #1E1E2E; padding: 20px; border-radius: 10px;
        margin-bottom: 15px; border: 1px solid #333; transition: 0.3s;
    }
    .pricing-card:hover { border-color: #00FF7F; box-shadow: 0 0 10px rgba(0, 255, 127, 0.2); }
    .pro-card { background-color: #1A2E22; border: 1px solid #00FF7F; }
    .card-title { color: #FFFFFF; font-size: 18px; font-weight: bold; margin-bottom: 10px; }
    .card-price { color: #00FF7F; font-size: 22px; font-weight: bold; margin-bottom: 15px; }
    .card-feature { color: #AAAAAA; font-size: 14px; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar) لمدخلات المستخدم
st.sidebar.image("https://upload.wikimedia.org/wikipedia/ar/thumb/a/a2/Taibah_University_Logo.svg/1200px-Taibah_University_Logo.svg.png", width=150)
st.sidebar.title("🎛️ لوحة التحكم الجغرافية")
st.sidebar.markdown("قم بتعديل أوزان المعايير لتحديث الخريطة التفاعلية:")

w_grid = st.sidebar.slider("🔌 القرب من شبكة الكهرباء (154/380 kV)", 0, 100, 30)
w_roads = st.sidebar.slider("🛣️ القرب من شبكة الطرق", 0, 100, 25)
w_pop = st.sidebar.slider("👥 الكثافة السكانية", 0, 100, 20)
w_poi = st.sidebar.slider("🛒 القرب من المراكز التجارية (POIs)", 0, 100, 15)
w_slope = st.sidebar.slider("⛰️ استواء التضاريس (Slope)", 0, 100, 10)

total_weight = w_grid + w_roads + w_pop + w_poi + w_slope
if total_weight > 0:
    weights = [w_grid/total_weight, w_roads/total_weight, w_pop/total_weight, w_poi/total_weight, w_slope/total_weight]
else:
    weights = [0.2, 0.2, 0.2, 0.2, 0.2]

# 3. المنطقة العلوية (المؤشرات الرئيسية كما في كودك القديم)
st.markdown("<h1 class='main-title'>⚡ التحليل المكاني الذكي لمحطات شحن المركبات بالمدينة المنورة</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="📍 المواقع المثلى المكتشفة", value=f"{int(total_weight * 1.5)} موقع", delta="محدث")
with col2:
    cr_value = max(0.01, abs(0.15 - (w_grid/200)))
    st.metric(label="📊 نسبة التناسق (CR)", value=f"{cr_value:.3f}", delta="-0.02" if cr_value < 0.1 else "+0.05", delta_color="inverse")
with col3:
    st.metric(label="🔋 الوفر المتوقع في الطاقة", value=f"{int(w_grid * 0.8)} %", delta="كفاءة عالية")
with col4:
    st.metric(label="⏱️ زمن معالجة الذكاء الاصطناعي", value="1.2 ثانية", delta="سريع")

st.divider()


# ==============================================================
# 4. التحديث الجديد: قسم الأعمدة الثلاثة (نتائج - خريطة - باقات)
# ==============================================================
col_results, col_map, col_plans = st.columns([1, 1.5, 1])

# 1. قراءة البيانات وحساب النتيجة الديناميكية (قبل عرضها في الأعمدة)
try:
    df = pd.read_csv('madinah_locations.csv')
    df['Dynamic_Score'] = (
        (df['Grid_Score'] * (w_grid / 100)) +
        (df['Road_Score'] * (w_roads / 100)) +
        (df['Pop_Score'] * (w_pop / 100)) +
        (df['POI_Score'] * (w_poi / 100)) +
        (df['Slope_Score'] * (w_slope / 100))
    )
    df_sorted = df.sort_values(by='Dynamic_Score', ascending=False)
    best_location = df_sorted.iloc[0]
    file_exists = True
except FileNotFoundError:
    file_exists = False

# --- العمود الأول: النتائج (يمين الشاشة) ---
with col_results:
    st.subheader("📊 1. تقييم المعايير")
    
    if file_exists:
        st.success(f"**الموقع الأمثل الموصى به: {best_location['Location_ID']}**")
        st.caption(f"بنسبة توافق: {best_location['Dynamic_Score']:.1f}%")
    else:
        st.error("ملف البيانات غير موجود.")
    
    st.markdown("**أوزان الملاءمة المكانية:**")
    st.caption(f"🔌 شبكة الكهرباء ({w_grid}%)")
    st.progress(int(w_grid))
    
    st.caption(f"🛣️ شبكة الطرق ({w_roads}%)")
    st.progress(int(w_roads))
    
    st.caption(f"👥 الكثافة السكانية ({w_pop}%)")
    st.progress(int(w_pop))
    
    st.caption(f"🛒 الأنشطة التجارية ({w_poi}%)")
    st.progress(int(w_poi))
    
    st.caption(f"⛰️ استواء التضاريس ({w_slope}%)")
    st.progress(int(w_slope))

# --- العمود الثاني: الخريطة (وسط الشاشة) ---
# --- العمود الثاني: الخريطة (وسط الشاشة) ---
with col_map:
    st.subheader("🗺️ 2. الخريطة الحرارية (Heatmap)")

    if file_exists:
        # التعديل هنا: جعل مركز الخريطة يطابق إحداثيات أفضل موقع لتتبعه الكاميرا تلقائياً
        dynamic_center = [best_location['Latitude'], best_location['Longitude']]
        m = folium.Map(location=dynamic_center, zoom_start=14, tiles='OpenStreetMap')
        
        # رسم الخريطة الحرارية بناءً على النتيجة الديناميكية
        heat_data = [[row['Latitude'], row['Longitude'], row['Dynamic_Score']] for index, row in df.iterrows()]
        HeatMap(heat_data, radius=15, blur=15, max_zoom=1).add_to(m)
        
        # وضع علامة خضراء بارزة جداً على أفضل موقع
        folium.Marker(
            dynamic_center,
            popup=f"أفضل موقع: {best_location['Location_ID']}",
            tooltip=f"الموقع الأمثل للاستثمار: {best_location['Location_ID']} (التقييم: {best_location['Dynamic_Score']:.1f}%)",
            icon=folium.Icon(color="green", icon="bolt", prefix='fa')
        ).add_to(m)
        
        # إضافة دائرة حمراء حول الموقع لتمييزه بشكل قاطع عن البقع الحرارية المحيطة
        folium.Circle(
            location=dynamic_center,
            radius=400,
            color='red',
            weight=3,
            fill=False
        ).add_to(m)

    else:
        # خريطة افتراضية في حال غياب الملف
        m = folium.Map(location=[24.4686, 39.6111], zoom_start=12, tiles='OpenStreetMap')

    st_folium(m, width=100, height=450, returned_objects=[], use_container_width=True)
# --- العمود الثالث: باقات الاستثمار (يسار الشاشة) ---
with col_plans:
    st.subheader("💼 3. باقات الاستثمار")
    st.markdown("""
    <div class="pricing-card">
        <div class="card-title">باقة الموقع المفرد (Starter)</div>
        <div class="card-feature">لأصحاب الأراضي والمستثمرين</div>
        <div class="card-price">999 ر.س / موقع</div>
        <div class="card-feature">✔️ فحص سعة المحول</div>
        <div class="card-feature">✔️ حساب الجدوى والعائد</div>
    </div>
    <div class="pricing-card pro-card">
        <div class="card-title">⭐ باقة مشغلي الشواحن (CPO Pro)</div>
        <div class="card-feature">لشركات شحن المركبات وسلاسل المحطات</div>
        <div class="card-price">3,499 ر.س / شهر</div>
        <div class="card-feature">✔️ خريطة المدينة كاملة وتنبؤات الطلب</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================
# 5. المنطقة السفلية: كودك القديم للرسوم البيانية (مقارنة AI و AHP)
# ==============================================================
st.subheader("📈 4. التحليل التقني للأوزان: الخبراء (AHP) مقابل الذكاء الاصطناعي (ML)")

col_chart1, col_chart2 = st.columns(2)
categories = ['شبكة الكهرباء', 'شبكة الطرق', 'الكثافة السكانية', 'المراكز التجارية', 'التضاريس']
current_weights = [w_grid, w_roads, w_pop, w_poi, w_slope]

# قراءة الأوزان من ملف الذكاء الاصطناعي (كما برمجتها سابقاً)
ai_weights_list = [20, 20, 20, 20, 20]
if os.path.exists('models/ai_weights.json'):
    with open('models/ai_weights.json', 'r', encoding='utf-8') as f:
        ai_data = json.load(f)
        ai_weights_list = [
            ai_data.get("شبكة الكهرباء", 20),
            ai_data.get("شبكة الطرق", 20),
            ai_data.get("الكثافة السكانية", 20),
            ai_data.get("المراكز التجارية", 20),
            ai_data.get("التضاريس", 20)
        ]

with col_chart1:
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
    fig_bar = go.Figure(data=[
        go.Bar(name='تفضيلات المستخدم (AHP)', x=categories, y=current_weights, marker_color='#3B82F6'),
        go.Bar(name='تعلم الآلة (Random Forest)', x=categories, y=ai_weights_list, marker_color='#10B981')
    ])
    fig_bar.update_layout(barmode='group', title="مقارنة الذكاء الاصطناعي بالتفضيلات البشرية")
    st.plotly_chart(fig_bar, use_container_width=True)

st.caption("تم تطوير هذا النموذج الأولي للمشاركة في مسابقة طيبة ثون 2026 - مسار الابتكار التقني والصناعي.")