import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go

# ==============================================================
# 1. إعدادات الصفحة والهوية البصرية الجديدة (GeoCharge AI)
# ==============================================================
st.set_page_config(
    page_title="GeoCharge AI | جيوشارج للذكاء الاصطناعي",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
    .stApp { direction: rtl; background-color: #0A111F; }
    
    .brand-title {
        text-align: center; background: linear-gradient(90deg, #00E676 0%, #00B4D8 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 3.5rem; font-weight: 900; margin-bottom: 0px; padding-bottom: 0px;
    }
    .brand-subtitle { text-align: center; color: #9CA3AF; font-size: 1.2rem; margin-top: -10px; margin-bottom: 30px; }
    
    .pricing-card {
        background-color: #121E36; padding: 20px; border-radius: 15px;
        margin-bottom: 15px; border: 1px solid #1F2D4A; transition: 0.3s;
    }
    .pricing-card:hover { border-color: #00B4D8; box-shadow: 0 0 15px rgba(0, 180, 216, 0.3); }
    .pro-card { background-color: #0D2B33; border: 1.5px solid #00E676; }
    .card-title { color: #FFFFFF; font-size: 20px; font-weight: 900; margin-bottom: 10px; }
    .card-price { color: #00E676; font-size: 24px; font-weight: bold; margin-bottom: 15px; }
    .card-feature { color: #B0BEC5; font-size: 15px; margin-bottom: 8px; }
    
    .ai-justification {
        background-color: #0A1929; border-right: 4px solid #00B4D8;
        padding: 15px; border-radius: 8px; color: #E0E0E0; font-size: 0.95rem; margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================
# 2. القائمة الجانبية وحساب الأوزان (الذكاء المكاني)
# ==============================================================
st.sidebar.image("logo_black_no_bg.png", use_container_width=True)
# text rather than image for the title
# st.sidebar.markdown("<h2 style='text-align:center; color:#00E676;'>GeoCharge AI</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("**محرك القرار (MCDA):**")

w_grid = st.sidebar.slider("⚡ القرب من شبكة الكهرباء", 0, 100, 35)
w_roads = st.sidebar.slider("🛣️ تدفق المرور", 0, 100, 25)
w_pop = st.sidebar.slider("👥 الكثافة السكانية", 0, 100, 15)
w_poi = st.sidebar.slider("🛒 الأنشطة التجارية", 0, 100, 15)
w_slope = st.sidebar.slider("⛰️ استواء التضاريس", 0, 100, 10)

# تطبيع الأوزان (Normalization)
total_weight = w_grid + w_roads + w_pop + w_poi + w_slope
if total_weight == 0: total_weight = 1 

n_grid = w_grid / total_weight
n_roads = w_roads / total_weight
n_pop = w_pop / total_weight
n_poi = w_poi / total_weight
n_slope = w_slope / total_weight

# مفتاح ذكي لتتبع تغييرات الأشرطة
slider_state = f"{w_grid}_{w_roads}_{w_pop}_{w_poi}_{w_slope}"

# ==============================================================
# 3. المنطقة العلوية
# ==============================================================
st.markdown("<h1 class='brand-title'>GeoCharge AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>جيوشارج للذكاء الاصطناعي | المنصة الذكية لقرارات النشر المكاني</p>", unsafe_allow_html=True)

col_k1, col_k2, col_k3, col_k4 = st.columns(4)
with col_k1: st.metric("📍 المواقع المرشحة", "3 مناطق كبرى", "بيانات جغرافية حقيقية")
with col_k2: st.metric("📊 موثوقية التحليل", "عالية", "خوارزميات AI")
with col_k3: st.metric("🔋 كفاءة العائد (ROI)", "مُحسّنة", "تحديث لحظي")
with col_k4: st.metric("⏱️ زمن اتخاذ القرار", "0.2 ثانية", "محرك تفاعلي")
st.divider()

# ==============================================================
# 4. البيانات الحقيقية وحساب الملاءمة
# ==============================================================
data = {
    'ID': ['P-01', 'P-02', 'P-03'],
    'Name': ['محيط النور مول (المنطقة المركزية التجارية)', 'محطة قطار الحرمين السريع', 'حديقة الملك فهد المركزية'],
    'Latitude': [24.49605, 24.47098, 24.4130],
    'Longitude': [39.59532, 39.69969, 39.6300],
    'Grid_Score': [85, 98, 70],
    'Road_Score': [90, 95, 65],
    'Pop_Score':  [80, 50, 85],
    'POI_Score':  [95, 70, 90],
    'Slope_Score':[90, 100, 80],
    'Justification': [
        "تم اختيار هذا الموقع بناءً على قربه المباشر من مجمع النور التجاري على طريق الملك عبدالله (الدائري الثاني). هذا الموقع يعتبر نقطة جذب هائلة للسكان، وهو مثالي لتطبيق استراتيجية (Destination Charging) حيث يمكن للزوار شحن مركباتهم أثناء التسوق.",
        "موقع استراتيجي يخدم محطة قطار الحرمين السريع. يتميز ببنية تحتية كهربائية هائلة للضغط العالي وارتباط مباشر بالطرق الإقليمية السريعة، مما يجعله الأنسب لتركيب شواحن فائقة السرعة (DC) لخدمة المسافرين عبر المدن.",
        "تم ترشيح هذا الموقع لكونه وجهة ترفيهية واسعة تقصدها العائلات لساعات طويلة. وبسبب كثافة الإقبال ومدة البقاء الطويلة، يعتبر هذا الموقع مثالياً لنشر شبكة من شواحن التيار المتردد (AC) الفعالة من حيث التكلفة."
    ]
}
df = pd.DataFrame(data)

# حساب النتيجة بعد التطبيع
df['Dynamic_Score'] = (
    (df['Grid_Score'] * n_grid) +
    (df['Road_Score'] * n_roads) +
    (df['Pop_Score']  * n_pop) +
    (df['POI_Score']  * n_poi) +
    (df['Slope_Score']* n_slope)
)
# ترتيب المواقع من الأفضل للأقل بناءً على المتغيرات الحية
df_sorted = df.sort_values(by='Dynamic_Score', ascending=False)

# ==============================================================
# 5. الأعمدة الثلاثة (النتائج التفاعلية - خريطة - باقات)
# ==============================================================
col_results, col_map, col_plans = st.columns([1, 1.5, 1])

with col_results:
    st.markdown("<h3 style='color:#00B4D8;'>1. استكشاف المواقع المرشحة</h3>", unsafe_allow_html=True)
    
    # السر هنا: نستخدم slider_state كمفتاح. كلما تغيرت الأشرطة، تتحدث القائمة لتختار الأفضل تلقائياً.
    selected_name = st.selectbox(
        "📌 المواقع مرتبة من الأفضل للأقل:", 
        df_sorted['Name'].tolist(),
        key=slider_state
    )
    
    # استخراج بيانات الموقع المختار
    selected_location = df[df['Name'] == selected_name].iloc[0]
    
    # التقييم
    score = min(int(selected_location['Dynamic_Score']), 100)
    st.markdown(f"<h2 style='text-align:center; color:#00E676; margin-top:10px;'>التقييم: {score:.1f}%</h2>", unsafe_allow_html=True)
    st.progress(score)
    
    # عرض المبرر المتغير
    st.markdown(f"""
        <div class="ai-justification">
            <b>تحليل الذكاء الاصطناعي للموقع:</b><br><br>
            {selected_location['Justification']}
        </div>
    """, unsafe_allow_html=True)

with col_map:
    st.markdown("<h3 style='color:#00B4D8;'>2. الخريطة التفاعلية (Live Map)</h3>", unsafe_allow_html=True)
    
    dynamic_center = [selected_location['Latitude'], selected_location['Longitude']]
    m = folium.Map(location=dynamic_center, zoom_start=14, tiles='OpenStreetMap')
    
    for index, row in df.iterrows():
        is_selected = (row['ID'] == selected_location['ID'])
        marker_color = "green" if is_selected else "blue"
        icon_type = "bolt" if is_selected else "info-sign"
        
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            popup=row['Name'],
            tooltip=f"{row['Name']} (تقييم: {row['Dynamic_Score']:.1f}%)",
            icon=folium.Icon(color=marker_color, icon=icon_type, prefix='fa')
        ).add_to(m)
        
        if is_selected:
            folium.Circle(
                location=[row['Latitude'], row['Longitude']],
                radius=400,
                color='red',
                weight=3,
                fill=False
            ).add_to(m)

    st_folium(m, width=100, height=450, returned_objects=[], use_container_width=True)

with col_plans:
    st.markdown("<h3 style='color:#00B4D8;'>3. نماذج الأعمال (Business Models)</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class="pricing-card">
        <div class="card-title">باقة أصحاب العقارات</div>
        <div class="card-feature">للمراكز التجارية، الفنادق، والمجمعات</div>
        <div class="card-price">تحليل الموقع وتحديد السعة</div>
        <div class="card-feature">✔️ فحص فني لمحولات شبكة الكهرباء</div>
        <div class="card-feature">✔️ دراسة الجدوى وتوقعات العائد المالي</div>
    </div>
    <div class="pricing-card pro-card">
        <div class="card-title">⭐ باقة مشغلي الشبكات (CPO)</div>
        <div class="card-feature">لشركات النقل ومستثمري البنية التحتية</div>
        <div class="card-price">رخصة وصول API لبيانات المدينة</div>
        <div class="card-feature">✔️ خريطة متكاملة وتنبؤات AI للطلب المستقبلي</div>
        <div class="card-feature">✔️ تكامل مع خطط الأمانة لنمو المدن الذكية</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==============================================================
# 6. التحليل التقني للموقع المُختار
# ==============================================================
st.markdown(f"<h3 style='color:#00B4D8; text-align:center;'>4. البصمة المكانية لـ: {selected_location['Name']}</h3>", unsafe_allow_html=True)

categories = ['سعة الكهرباء', 'شبكة الطرق', 'الكثافة السكانية', 'الأنشطة التجارية', 'استواء الأرض']
selected_scores = [selected_location['Grid_Score'], selected_location['Road_Score'], selected_location['Pop_Score'], selected_location['POI_Score'], selected_location['Slope_Score']]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=selected_scores,
    theta=categories,
    fill='toself',
    name=selected_location['Name'],
    line_color='#00E676'
))
fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100], gridcolor="#1F2D4A"),
        bgcolor="#0A111F"
    ),
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#B0BEC5', family='Cairo')
)
st.plotly_chart(fig_radar, use_container_width=True)