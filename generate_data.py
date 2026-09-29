import pandas as pd
import numpy as np

# تحديد إحداثيات تقريبية تغطي أحياء المدينة المنورة
np.random.seed(42)
data_size = 100

data = {
    'Location_ID': [f'P-{str(i).zfill(3)}' for i in range(1, data_size + 1)],
    'Latitude': np.random.uniform(24.42, 24.52, data_size),
    'Longitude': np.random.uniform(39.55, 39.68, data_size),
    # تقييم كل موقع من 0 إلى 100 بناءً على دراسة افتراضية لبيانات GIS
    'Grid_Score': np.random.randint(40, 100, data_size),   # القرب من الكهرباء
    'Road_Score': np.random.randint(50, 100, data_size),   # القرب من الطرق
    'Pop_Score': np.random.randint(20, 100, data_size),    # الكثافة السكانية
    'POI_Score': np.random.randint(10, 100, data_size),    # الأنشطة التجارية
    'Slope_Score': np.random.randint(60, 100, data_size)   # استواء الأرض (أعلى = أرض مستوية)
}

# تحويل البيانات إلى جدول وحفظها كملف CSV
df = pd.DataFrame(data)
df.to_csv('madinah_locations.csv', index=False, encoding='utf-8')

print("✅ تم إنشاء ملف 'madinah_locations.csv' بنجاح ويحتوي على 100 موقع!")