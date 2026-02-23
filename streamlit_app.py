import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import time

st.set_page_config(page_title="MapInsight | النسخة الدقيقة", layout="wide", page_icon="📍")

st.title("📍 محدد المواقع السعودي الدقيق")
st.write("تم تحديث خوارزمية البحث لضمان عدم تداخل المدن المتجاورة.")

uploaded_file = st.file_uploader("ارفع ملف CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    
    c1, c2, c3 = st.columns(3)
    with c1: name_col = st.selectbox("اسم العميل", df.columns)
    with c2: city_col = st.selectbox("المدينة", df.columns)
    with c3: addr_col = st.selectbox("العنوان", df.columns)

    if st.button("🚀 تحليل وتوليد الخريطة"):
        geolocator = Nominatim(user_agent="saudi_ultra_mapper_v8")
        m = folium.Map(location=[24.7136, 46.6753], zoom_start=5)
        
        # تعريف حدود تقريبية للمدن الكبرى لمنع التداخل (Latitude, Longitude)
        city_bounds = {
            "مكة": ["21.20", "39.50", "21.60", "40.10"],
            "مكة المكرمة": ["21.20", "39.50", "21.60", "40.10"],
            "جدة": ["21.20", "38.90", "21.90", "39.40"],
            "الرياض": ["24.40", "46.40", "25.00", "47.00"],
            "الطائف": ["21.10", "40.20", "21.50", "40.60"]
        }

        found_count = 0
        failed_names = []
        progress_bar = st.progress(0)

        for i, row in df.iterrows():
            time.sleep(1.2)
            progress_bar.progress((i + 1) / len(df))
            
            city = str(row[city_col]).strip()
            address = str(row[addr_col]).strip()
            query = f"{address}, {city}, Saudi Arabia"
            
            # محاولة البحث مع تقييد النطاق الجغرافي للمدينة
            viewbox = city_bounds.get(city, None)
            
            try:
                if viewbox:
                    # يبحث فقط داخل حدود المدينة المحددة
                    location = geolocator.geocode(query, viewbox=[(viewbox[0], viewbox[1]), (viewbox[2], viewbox[3])], bounded=True, timeout=10)
                else:
                    location = geolocator.geocode(query, timeout=10)

                if location:
                    folium.Marker(
                        [location.latitude, location.longitude],
                        popup=f"<b>{row[name_col]}</b><br>{city}",
                        tooltip=row[name_col],
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(m)
                    found_count += 1
                else:
                    failed_names.append(row[name_col])
            except:
                failed_names.append(row[name_col])

        progress_bar.empty()
        st.write(f"✅ تم تحديد {found_count} موقع بنجاح.")
        folium_static(m, width=1200, height=600)

        if failed_names:
            with st.expander("⚠️ أسماء لم يتم تحديدها:"):
                st.write(", ".join(failed_names))
