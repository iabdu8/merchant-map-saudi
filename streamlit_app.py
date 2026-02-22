import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="منصة تحليل التجار", layout="wide")

st.title("📍 محول عناوين العملاء إلى خريطة تفاعلية")

uploaded_file = st.file_uploader("اختر ملف CSV", type=["csv"])

if uploaded_file:
df = pd.read_csv(uploaded_file, encoding='utf-8')
st.success("تم رفع الملف بنجاح!")
