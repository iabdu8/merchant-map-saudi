import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import time
import io

# 1. إعدادات الهوية البصرية للموقع
st.set_page_config(page_title="MapInsight | محلل بيانات التجار", layout="wide", page_icon="📍")

# تنسيق جمالي باستخدام CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. الهيدر (العنوان)
st.title("📍 منصة MapInsight لتحليل المواقع الجغرافية")
st.subheader("حول بيانات عملائك إلى رؤى تسويقية واضحة")
st.write("---")

# 3. شريط جانبي للتعليمات
with st.sidebar:
    st.header("كيفية الاستخدام")
    st.info("""
    1. ارفع ملف CSV (مستخرج من سلة أو زد).
    2. حدد الأعمدة الصحيحة.
    3. اضغط 'توليد' لمشاهدة خريطة عملائك.
    """)
    st.write("---")
    st.caption("تطوير: منصة MapInsight الذكية")

# 4. رفع الملف ومعالجته
uploaded_file = st.file_uploader("قم بسحب وإفلات ملف مبيعاتك هنا", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    
    # واجهة عرض البيانات الأولية
    with st.expander("👁️ عرض البيانات المرفوعة"):
        st.dataframe(df.head())

    # اختيار الأعمدة في حاوية منظمة
    st.write("### 🛠️ إعدادات الخريطة")
    c1, c2, c3 = st.columns(3)
    with c1: name_col = st.selectbox("👤 اسم العميل", df.columns)
    with c2: city_col = st.selectbox("🏙️ المدينة", df.columns)
    with c3: addr_col = st.selectbox("🏠 الحي / العنوان", df.columns)

    if st.button("🚀 توليد الخريطة والتحليل الذكي"):
        geolocator = Nominatim(user_agent="mapinsight_pro_v1")
        m = folium.Map(location=[24.7136, 46.6753], zoom_start=5, tiles='cartodbpositron')
        marker_cluster = MarkerCluster().add_to(m)
        
        found_count = 0
        failed_names = []
        
        # شريط تقدم أنيق
        progress_text = "جاري تحليل العناوين وتحويلها لإحداثيات..."
        my_bar = st.progress(0, text=progress_text)

        for i, row in df.iterrows():
            time.sleep(1.1) # لضمان استقرار المحرك المجاني
            my_bar.progress((i + 1) / len(df))
            
            query = f"{row[addr_col]}, {row[city_col]}, Saudi Arabia"
            try:
                location = geolocator.geocode(query, timeout=10)
                if location and (row[city_col].strip() in location.address):
                    folium.Marker(
                        [location.latitude, location.longitude],
                        popup=f"<b>العميل:</b> {row[name_col]}<br><b>الحي:</b> {row[addr_col]}",
                        tooltip=row[name_col],
                        icon=folium.Icon(color='blue', icon='shopping-cart', prefix='fa')
                    ).add_to(marker_cluster)
                    found_count += 1
                else:
                    failed_names.append(row[name_col])
            except:
                failed_names.append(row[name_col])

        my_bar.empty()

        # 5. عرض الإحصائيات (Dashboard بسيط)
        st.write("### 📊 ملخص التحليل")
        res1, res2, res3 = st.columns(3)
        res1.metric("إجمالي العملاء", len(df))
        res2.metric("تم تحديدهم", found_count)
        res3.metric("مدن التغطية", df[city_col].nunique())

        # 6. عرض الخريطة
        st.write("### 🗺️ خريطة توزيع العملاء")
        folium_static(m, width=1200, height=600)

        # 7. زر تحميل الخريطة كملف HTML للتاجر
        map_html = m._repr_html_()
        st.download_button(
            label="💾 تحميل الخريطة كملف تفاعلي (HTML)",
            data=map_html,
            file_name="customer_map.html",
            mime="text/html"
        )

        if failed_names:
            with st.expander("⚠️ عملاء لم تظهر مواقعهم (اضغط للتفاصيل)"):
                st.write("قد تكون هذه العناوين غير دقيقة في قاعدة بيانات الخرائط:")
                st.write(", ".join(failed_names))
        
        st.balloons()
else:
    # رسالة ترحيبية قبل رفع الملف
    st.warning("👈 يرجى رفع ملف CSV من القائمة الجانبية للبدء.")
    st.image("https://img.freepik.com/free-vector/map-location-concept-illustration_114360-146.jpg", width=400)
