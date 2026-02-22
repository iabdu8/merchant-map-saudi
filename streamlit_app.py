import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import time  # مكتبة التحكم بالوقت لضمان عدم تخطي العناوين

# إعداد الصفحة
st.set_page_config(page_title="منصة تحليل التجار", layout="wide")

st.title("📍 محول العناوين إلى خريطة تفاعلية (نسخة التجار)")
st.write("ارفع ملف مبيعاتك لترى توزيع عملائك بدقة.")

# رفع الملف
uploaded_file = st.file_uploader("اختر ملف CSV المستخرج من سلة أو زد", type=["csv"])

if uploaded_file:
    # قراءة البيانات مع دعم العربية
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.success(f"تم رفع {len(df)} عميل بنجاح!")
    
    # اختيار الأعمدة
    col1, col2, col3 = st.columns(3)
    with col1:
        name_col = st.selectbox("عمود اسم العميل:", df.columns)
    with col2:
        city_col = st.selectbox("عمود المدينة:", df.columns)
    with col3:
        address_col = st.selectbox("عمود الحي / العنوان:", df.columns)

    if st.button("توليد الخريطة الآن"):
        # إعداد محرك البحث
        geolocator = Nominatim(user_agent="saudi_merchant_pro_v3")
        
        # إنشاء الخريطة (مركزها السعودية)
        m = folium.Map(location=[24.7136, 46.6753], zoom_start=5)
        
        # شريط تقدم للعملية
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        found_count = 0
        
        for i, row in df.iterrows():
            # تحديث شريط التقدم
            progress = (i + 1) / len(df)
            progress_bar.progress(progress)
            status_text.text(f"جاري البحث عن موقع العميل: {row[name_col]}...")
            
            # تركيب العنوان
            full_address = f"{row[address_col]}, {row[city_col]}, Saudi Arabia"
            
            try:
                location = geolocator.geocode(full_address)
                if location:
                    folium.Marker(
                        [location.latitude, location.longitude],
                        popup=f"العميل: {row[name_col]}",
                        tooltip=row[name_col],
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(m)
                    found_count += 1
                
                # إضافة ثانية واحدة انتظار بين كل عميل لضمان عدم حظر المحرك
                time.sleep(1) 
                
            except:
                continue
        
        status_text.text(f"اكتملت المعالجة! تم تحديد {found_count} موقع من أصل {len(df)}")
        
        # عرض الخريطة بشكل ثابت
        folium_static(m, width=1000, height=600)
        
else:
    st.info("بانتظار رفع ملف البيانات لبدء التحليل.")
