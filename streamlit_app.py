import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import time

st.set_page_config(page_title="منصة مَـدَى | للتحليل الجغرافي", layout="wide", page_icon="📍")

st.markdown("""
<style>
.main { background-color: #fdfdfd; }
.stButton>button {
background-image: linear-gradient(to right, #1e3c72, #2a5298);
color: white; border-radius: 12px; font-weight: bold; border: none; height: 3em;
}
.info-box { padding: 20px; border-radius: 10px; background-color: #e3f2fd; border-right: 5px solid #1e3c72; text-align: right; }
</style>
""", unsafe_allow_html=True)

st.title("📍 منصة مَـدَى الذكية")
st.markdown("<p style='text-align: right; font-size: 1.2rem; color: #555;'>حول بيانات عملائك إلى خريطة تفاعلية واحترافية</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("ارفع ملف مبيعاتك بصيغة CSV", type=["csv"])

if uploaded_file:
df = pd.read_csv(uploaded_file, encoding='utf-8')

else:
st.markdown("<div class='info-box'>يرجى رفع ملف CSV للبدء في التحليل.</div>", unsafe_allow_html=True)
