import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة (يجب أن تكون الشاشة عريضة لتدعم 3 أعمدة)
st.set_page_config(
    page_title="GeoCharge.AI | طيبة ثون",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed" # إخفاء القائمة الجانبية لإعطاء مساحة للشاشات الثلاث
)

# 2. تخصيص التصميم والألوان (CSS) ليطابق الصورة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
    }
    
    /* عكس اتجاه الصفحة ليدعم اللغة العربية من اليمين لليسار */
    .stApp {
        direction: rtl;
    }
    
    /* تصميم بطاقات باقات الاستثمار */
    .pricing-card {
        background-color: #1E1E2E;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #333;
        transition: 0.3s;
    }
    .pricing-card:hover {
        border-color: #00FF7F;
        box-shadow: 0 0 10px rgba(0, 255, 127, 0.2);
    }
    .pro-card {
        background-color: #23352A;
        border: 1px solid #00FF7F;
    }
    .card-title {
        color: #FFFFFF;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .card-price {
        color: #00FF7F;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .card-feature {
        color: #AAAAAA;
        font-size: 14px;
        margin-bottom: 5px;
    }
    
    /* تصميم العناوين الرئيسية */
    .main-header {
        text-align: center;
        color: #FFFFFF;
        padding-bottom: 10px;
    }
    .sub-header {
        text-align: center;
        color: #AAAAAA;
        margin-bottom: 30px;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. العنوان الرئيسي للمنصة
st.markdown("<h1 class='main-header'>GeoCharge.AI - محاكاة تجربة المستثمر والمخطط</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>النتائج المثلى، الخريطة التفاعلية، وباقات الاستثمار لمدينة ذكية</p>", unsafe_allow_html=True)

st.divider()

# 4. تقسيم الشاشة إلى 3 أعمدة رئيسية
# العمود الأول (اليمين): النتائج / العمود الثاني (الوسط): الخريطة / العمود الثالث (اليسار): الباقات
col_results, col_map, col_plans = st.columns([1, 1.5, 1])

# ==========================================
# العمود الأول: نتائج المعايير (يمين الشاشة)
# ==========================================
with col_results:
    st.subheader("📊 1. نتائج المعايير")
    
    # مربع النتيجة الكبيرة
    st.success("**الموقع الموصى به: P-01**")
    st.metric(label="مؤشر الملاءمة المكانية (CSI)", value="94.6 / 100", delta="جاهز للاستثمار")
    
    st.markdown("---")
    st.markdown("**تقييم معايير الذكاء الاصطناعي:**")
    
    # محاكاة لأشرطة التقدم (Progress Bars) التي ظهرت في صورتك
    st.caption("👥 الكثافة السكانية والطلب (91%)")
    st.progress(91)
    
    st.caption("🛣️ شبكة الطرق وتدفق المرور (89%)")
    st.progress(89)
    
    st.caption("🛒 نقاط الجذب والأنشطة التجارية (75%)")
    st.progress(75)
    
    st.caption("⚡ محطات وسعة شبكة الكهرباء (85%)")
    st.progress(85)


# ==========================================
# العمود الثاني: الخريطة التفاعلية (وسط الشاشة)
# ==========================================
with col_map:
    st.subheader("🗺️ 2. خريطة المواقع المقترحة")
    st.caption("🟢 متصل ببيانات GIS | المواقع المتوافقة مع سعة الشبكة")
    
    # إنشاء خريطة بخلفية داكنة لتناسب التصميم
    m = folium.Map(location=[24.4686, 39.6111], zoom_start=13, tiles='CartoDB dark_matter')
    
    # إضافة النقطة P-01 (الموقع الأمثل)
    folium.Marker(
        [24.4686, 39.6111],
        popup="الموقع الأمثل P-01",
        tooltip="P-01 الموقع الأمثل للاستثمار (94.6%)",
        icon=folium.Icon(color="green", icon="bolt", prefix='fa')
    ).add_to(m)
    
    # إضافة نقطة أخرى بديلة
    folium.Marker(
        [24.4500, 39.6200],
        popup="موقع بديل P-02",
        tooltip="P-02 موقع بديل (88.2%)",
        icon=folium.Icon(color="purple", icon="info-sign")
    ).add_to(m)

    # عرض الخريطة
    st_folium(m, width=100, height=450, returned_objects=[], use_container_width=True)


# ==========================================
# العمود الثالث: باقات الاستثمار (يسار الشاشة)
# ==========================================
with col_plans:
    st.subheader("💼 3. باقات الاستثمار")
    
    # باقة 1: Starter
    st.markdown("""
    <div class="pricing-card">
        <div class="card-title">باقة الموقع المفرد (Starter)</div>
        <div class="card-feature">لأصحاب الأراضي والمستثمرين الأفراد</div>
        <div class="card-price">999 ر.س / موقع</div>
        <div class="card-feature">✔️ فحص سعة المحول</div>
        <div class="card-feature">✔️ حساب الجدوى والعائد</div>
    </div>
    """, unsafe_allow_html=True)
    
    # باقة 2: Pro (المميزة)
    st.markdown("""
    <div class="pricing-card pro-card">
        <div class="card-title">⭐ باقة مشغلي الشواحن (CPO Pro)</div>
        <div class="card-feature">لشركات شحن المركبات وسلاسل المحطات</div>
        <div class="card-price">3,499 ر.س / شهر</div>
        <div class="card-feature">✔️ خريطة المدينة كاملة</div>
        <div class="card-feature">✔️ تنبؤات الطلب بالذكاء الاصطناعي</div>
    </div>
    """, unsafe_allow_html=True)
    
    # باقة 3: Enterprise
    st.markdown("""
    <div class="pricing-card">
        <div class="card-title">باقة المخطط الحضري (Enterprise)</div>
        <div class="card-feature">للأمانات، هيئات التطوير، ووزارة الطاقة</div>
        <div class="card-price">ترخيص سنوي مخصص</div>
        <div class="card-feature">✔️ نمذجة GIS غير محدودة</div>
        <div class="card-feature">✔️ تكامل مباشر مع API</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("اختر باقتك وابدأ نشر المحطات 🚀", use_container_width=True):
        st.success("تم تسجيل طلبك بنجاح!")