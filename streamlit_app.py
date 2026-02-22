import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import time

st.set_page_config(page_title="منصة تحليل التجار", layout="wide")
st.title("📍 محول العناوين الذكي")

uploaded_file = st.file_uploader("ارفع ملف CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.success(f"تم رفع {len(df)} عملاء.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        name_col = st.selectbox("اسم العميل:", df.columns)
    with col2:
        city_col = st.selectbox("المدينة:", df.columns)
    with col3:
        address_col = st.selectbox("الحي / العنوان:", df.columns)

    if st.button("توليد الخريطة الآن"):
        geolocator = Nominatim(user_agent="saudi_smart_search_v4")
        m = folium.Map(location=[24.7136, 46.6753], zoom_start=5)
        
        progress_bar = st.progress(0)
        found_count = 0
        
        for i, row in df.iterrows():
            progress_bar.progress((i + 1) / len(df))
            
            # محاولات بحث مختلفة لضمان النتيجة
            search_queries = [
                f"{row[address_col]}, {row[city_col]}, Saudi Arabia",
                f"{row[address_col]}, Saudi Arabia",
                f"{row[address_col]} {row[city_col]}"
            ]
            
            location = None
            for query in search_queries:
                try:
                    location = geolocator.geocode(query, timeout=10)
                    if location:
                        break # إذا وجد العنوان يتوقف عن المحاولات الأخرى
                except:
                    continue
                time.sleep(0.5) # وقت قصير جداً بين المحاولات
            
            if location:
                folium.Marker(
                    [location.latitude, location.longitude],
                    popup=f"{row[name_col]} - {row[address_col]}",
                    icon=folium.Icon(color='red')
                ).add_to(m)
                found_count += 1
            
            time.sleep(1) # وقت انتظار بين كل عميل وآخر

        st.write(f"✅ تم تحديد {found_count} من أصل {len(df)} بنجاح!")
        folium_static(m, width=1000, height=600)
