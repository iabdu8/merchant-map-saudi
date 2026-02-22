import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="منصة تحليل التجار", layout="wide")
st.title("📍 محول العناوين إلى خريطة تفاعلية")

uploaded_file = st.file_uploader("اختر ملف CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.success("تم رفع الملف بنجاح!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        name_col = st.selectbox("اسم العميل:", df.columns)
    with col2:
        city_col = st.selectbox("المدينة:", df.columns)
    with col3:
        address_col = st.selectbox("الحي / العنوان:", df.columns)

    if st.button("توليد الخريطة"):
        geolocator = Nominatim(user_agent="saudi_merchant_app_final")
        m = folium.Map(location=[24.7136, 46.6753], zoom_start=5)
        
        with st.spinner('جاري معالجة العناوين...'):
            for i, row in df.iterrows():
                full_address = f"{row[address_col]}, {row[city_col]}, Saudi Arabia"
                try:
                    location = geolocator.geocode(full_address)
                    if location:
                        folium.Marker(
                            [location.latitude, location.longitude],
                            popup=f"العميل: {row[name_col]}",
                            icon=folium.Icon(color='red')
                        ).add_to(m)
                except:
                    continue
            
            folium_static(m, width=1000, height=500)
            st.info("تم تثبيت الخريطة بنجاح!")
