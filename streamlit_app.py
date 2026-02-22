import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="تحليل تجار سلة وزد", layout="wide")

st.title("📍 منصة تحليل المواقع الجغرافية للتجار")
st.markdown("---")

# رفع الملف من قبل التاجر
uploaded_file = st.file_uploader("ارفع ملف الطلبات (CSV) المستخرج من سلة أو زد", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("معاينة البيانات:", df.head(3))
    
    cols = df.columns.tolist()
    # التاجر يختار الأعمدة المناسبة
    address_col = st.selectbox("اختر عمود (العنوان أو الحي):", cols)
    city_col = st.selectbox("اختر عمود (المدينة):", cols)
    name_col = st.selectbox("اختر عمود (اسم العميل) لإظهاره على الخريطة:", cols)

    if st.button("توليد خريطة العملاء"):
        geolocator = Nominatim(user_agent="saudi_merchant_app")
        m = folium.Map(location=[24.7136, 46.6753], zoom_start=5)
        
        with st.spinner('جاري قراءة العناوين وتحويلها لنقاط...'):
            for i, row in df.iterrows():
                # دمج الحي مع المدينة والسعودية لضمان أدق نتيجة
                full_address = f"{row[address_col]}, {row[city_col]}, Saudi Arabia"
                try:
                    location = geolocator.geocode(full_address)
                    if location:
                        folium.Marker(
                            [location.latitude, location.longitude],
                            popup=f"العميل: {row[name_col]}<br>العنوان: {row[address_col]}",
                            icon=folium.Icon(color='blue', icon='shopping-cart', prefix='fa')
                        ).add_to(m)
                except:
                    continue
        
        st_folium(m, width="100%", height=600)
        st.success("تم تحليل مواقع العملاء بنجاح!")