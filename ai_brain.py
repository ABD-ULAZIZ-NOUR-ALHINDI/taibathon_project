import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import json
import os

def train_spatial_ai_model():
    print("🚀 بدء تدريب نموذج الذكاء الاصطناعي المكاني...")
    
    # 1. إنشاء مجلد لحفظ المخرجات إذا لم يكن موجوداً
    os.makedirs('models', exist_ok=True)

    # 2. جلب البيانات المكانية
    # ملاحظة: هنا نستخدم بيانات محاكاة (Mock Data). 
    # في الهاكاثون الفعلي، ستستبدل هذا الكود بقراءة ملفات GIS الحقيقية باستخدام Geopandas
    # مثال: df = geopandas.read_file('data/madinah_grid.geojson')
    
    np.random.seed(42)
    data_size = 1000 # ألف مربع جغرافي افتراضي في المدينة المنورة
    
    df = pd.DataFrame({
        'Grid_ID': range(data_size),
        'Dist_to_Grid': np.random.uniform(10, 2000, data_size),   # القرب من الكهرباء (بالمتر)
        'Dist_to_Road': np.random.uniform(5, 1000, data_size),    # القرب من الطرق
        'Population_Density': np.random.uniform(100, 5000, data_size), # الكثافة السكانية
        'POIs_Count': np.random.randint(0, 20, data_size),        # عدد المراكز التجارية
        'Slope_Angle': np.random.uniform(0, 15, data_size),       # درجة الانحدار التضاريسي
        
        # التقييم التاريخي لنجاح الموقع (متغير مستهدف للتدريب)
        'Historical_Success_Score': np.random.uniform(20, 100, data_size) 
    })

    # 3. تحديد الميزات (X) والمتغير المستهدف (y)
    features = ['Dist_to_Grid', 'Dist_to_Road', 'Population_Density', 'POIs_Count', 'Slope_Angle']
    X = df[features]
    y = df['Historical_Success_Score']

    # 4. تدريب خوارزمية الغابات العشوائية
    print("🧠 جاري تحليل البيانات وبناء الغابات العشوائية...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X, y)

    # 5. استخراج الأهمية النسبية لكل معيار (Feature Importance)
    # تحويل القيم إلى نسب مئوية مجموعها 100
    importances = rf_model.feature_importances_ * 100
    
    # ترتيب الأوزان بنفس الترتيب الموجود في واجهة Streamlit
    ai_weights_dict = {
        "شبكة الكهرباء": round(importances[0], 1),
        "شبكة الطرق": round(importances[1], 1),
        "الكثافة السكانية": round(importances[2], 1),
        "المراكز التجارية": round(importances[3], 1),
        "التضاريس": round(importances[4], 1)
    }

    # 6. حفظ النتائج في ملف JSON ليقرأه ملف app.py
    with open('models/ai_weights.json', 'w', encoding='utf-8') as f:
        json.dump(ai_weights_dict, f, ensure_ascii=False, indent=4)
        
    print("✅ تم استخراج الأوزان بنجاح وحفظها في models/ai_weights.json!")
    print("📊 الأوزان المستخرجة من الذكاء الاصطناعي:")
    for k, v in ai_weights_dict.items():
        print(f"   - {k}: {v}%")

if __name__ == "__main__":
    train_spatial_ai_model()