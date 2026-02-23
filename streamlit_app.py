import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import time

# 1. إعدادات الصفحة (اختاري الاسم الذي أعجبكِ هنا)
st.set_page_config(page_title="مدى | لتحليل بيانات العملاء", layout="wide", page_icon="📍")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007bff; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("📍 منصة مَـدَى الذكية")
st.subheader("اكتشف أماكن تمركز عملائك بضغطة زر")

# 2. رفع الملف
uploaded_file = st.file_uploader("ارفع ملف مبيعاتك (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    
    st.write("### 🛠️ إعدادات الأعمدة")
    c1, c2, c3 = st.columns(3)
    with c1: name_col = st.selectbox("👤 اسم العميل", df.columns)
    with c2: city_col = st.selectbox("🏙️ المدينة", df.columns)
    with c3: addr_col = st.selectbox("🏠 الحي / العنوان", df.columns)

    if st.button("🚀 تحليل وتوليد الخريطة"):
        geolocator = Nominatim(user_agent="mada_precision_v9")
        
        # إنشاء الخريطة
        m = folium.Map(location=[24.7136, 46.6753], zoom_start=5)
        
        found_count = 0
        failed_names = []
        progress_bar = st.progress(0)

        for i, row in df.iterrows():
            time.sleep(1.2)
            progress_bar.progress((i + 1) / len(df))
            
            # تنظيف البيانات
            name = str(row[name_col]).strip()
            city = str(row[city_col]).strip()
            district = str(row[addr_col]).strip()
            
            query = f"{district}, {city}, Saudi Arabia"
            
            try:
                location = geolocator.geocode(query, timeout=10)
                if location and (city.lower() in location.address.lower()):
                    
                    # صياغة النص الذي سيظهر عند مرور الماوس (Tooltip)
                    info_text = f"الاسم: {name} | المدينة: {city} | الحي: {district}"
                    
                    folium.Marker(
                        [location.latitude, location.longitude],
                        # هذه الميزة تظهر المعلومات عند مرور الماوس
                        tooltip=info_text, 
                        # هذه تظهر عند الضغط (اختياري)
                        popup=f"<b>العميل:</b> {name}<br><b>العنوان:</b> {district}",
                        icon=folium.Icon(color='red', icon='user', prefix='fa')
                    ).add_to(m)
                    found_count += 1
                else:
                    failed_names.append(name)
            except:
                failed_names.append(name)

        progress_bar.empty()

        st.write(f"### ✅ تم تحديد {found_count} عميل على الخريطة")
        folium_static(m, width=1200, height=600)

        # زر التحميل
        map_html = m._repr_html_()
        st.download_button("💾 تحميل هذه الخريطة", data=map_html, file_name="mada_analysis.html", mime="text/html")

        if failed_names:
            with st.expander("⚠️ عملاء لم يتم تحديد مواقعهم بدقة:"):
                st.write(", ".join(failed_names))
        
        st.balloons()
