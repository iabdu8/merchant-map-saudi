import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="MapInsight | محلل بيانات التجار", layout="wide", page_icon="📍")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007bff; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("📍 منصة MapInsight")
st.subheader("عرض كامل نقاط البيع وتوزيع العملاء")

# 2. رفع الملف
uploaded_file = st.file_uploader("ارفع ملف مبيعاتك (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    
    st.write("### 🛠️ إعدادات الأعمدة")
    c1, c2, c3 = st.columns(3)
    with c1: name_col = st.selectbox("👤 اسم العميل", df.columns)
    with c2: city_col = st.selectbox("🏙️ المدينة", df.columns)
    with c3: addr_col = st.selectbox("🏠 الحي / العنوان", df.columns)

    if st.button("🚀 عرض الخريطة الشاملة"):
        geolocator = Nominatim(user_agent="mapinsight_v6_final")
        
        # إنشاء الخريطة
        m = folium.Map(location=[24.7136, 46.6753], zoom_start=5, tiles='OpenStreetMap')
        
        found_count = 0
        failed_names = []
        progress_bar = st.progress(0)

        for i, row in df.iterrows():
            time.sleep(1) # لضمان عدم حظر المحرك المجاني
            progress_bar.progress((i + 1) / len(df))
            
            query = f"{row[addr_col]}, {row[city_col]}, Saudi Arabia"
            try:
                location = geolocator.geocode(query, timeout=10)
                if location and (row[city_col].strip() in location.address):
                    # إضافة الدبوس مباشرة للخريطة (بدون تجميع)
                    folium.Marker(
                        [location.latitude, location.longitude],
                        popup=f"<b>الاسم:</b> {row[name_col]}<br><b>العنوان:</b> {row[addr_col]}",
                        tooltip=row[name_col],
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(m)
                    found_count += 1
                else:
                    failed_names.append(row[name_col])
            except:
                failed_names.append(row[name_col])

        progress_bar.empty()

        # عرض النتائج
        st.write(f"### ✅ تم تحديد {found_count} موقع بنجاح")
        folium_static(m, width=1200, height=600)

        # زر التحميل للتاجر
        map_html = m._repr_html_()
        st.download_button("💾 تحميل الخريطة كاملة", data=map_html, file_name="full_map.html", mime="text/html")

        if failed_names:
            with st.expander("⚠️ أسماء لم تظهر (تأكد من دقة العنوان)"):
                st.write(", ".join(failed_names))
        
        st.balloons()
