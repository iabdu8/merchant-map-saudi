import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import time

# إعداد الصفحة
st.set_page_config(page_title="منصة تحليل التجار الذكية", layout="wide")

st.title("📍 محول العناوين الجغرافي (النسخة الدقيقة)")
st.markdown("""
*هذه النسخة مصممة لضمان بقاء العميل داخل مدينته المحددة وتجنب أخطاء المواقع المتشابهة.*
""")

# رفع الملف
uploaded_file = st.file_uploader("ارفع ملف مبيعاتك (CSV)", type=["csv"])

if uploaded_file:
    # قراءة البيانات
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.success(f"تم رفع {len(df)} سجل بنجاح.")
    
    # اختيار الأعمدة
    col1, col2, col3 = st.columns(3)
    with col1:
        name_col = st.selectbox("اسم العميل:", df.columns)
    with col2:
        city_col = st.selectbox("المدينة:", df.columns)
    with col3:
        address_col = st.selectbox("الحي / العنوان:", df.columns)

    if st.button("توليد الخريطة وتحليل المواقع"):
        # إعداد المحرك مع تعريف فريد
        geolocator = Nominatim(user_agent="saudi_pro_merchant_mapper")
        
        # إنشاء الخريطة
        m = folium.Map(location=[24.7136, 46.6753], zoom_start=5)
        
        progress_bar = st.progress(0)
        found_count = 0
        failed_addresses = []

        for i, row in df.iterrows():
            # تحديث شريط التقدم
            progress = (i + 1) / len(df)
            progress_bar.progress(progress)
            
            # صياغة بحث "صارمة" (الحي + المدينة + السعودية) لمنع الهروب لمدن أخرى
            query = f"{row[address_col]}, {row[city_col]}, Saudi Arabia"
            
            try:
                # البحث عن الموقع
                location = geolocator.geocode(query, timeout=10)
                
                # شرط إضافي: التأكد أن المدينة المذكورة في الملف موجودة في نتيجة البحث
                if location and (row[city_col].strip() in location.address):
                    folium.Marker(
                        [location.latitude, location.longitude],
                        popup=f"<b>العميل:</b> {row[name_col]}<br><b>العنوان:</b> {row[address_col]}",
                        tooltip=f"{row[name_col]} - {row[city_col]}",
                        icon=folium.Icon(color='red', icon='user', prefix='fa')
                    ).add_to(m)
                    found_count += 1
                else:
                    failed_addresses.append(row[name_col])
                
                # تأخير بسيط جداً لاحترام قوانين المحرك المجاني
                time.sleep(1.2)
                
            except:
                failed_addresses.append(row[name_col])
                continue

        # النتائج
        st.write(f"### النتيجة: تم تحديد {found_count} موقع بنجاح ✅")
        
        if failed_addresses:
            with st.expander("أسماء عملاء لم يتم العثور على مواقعهم بدقة:"):
                for name in failed_addresses:
                    st.write(f"❌ {name}")
                st.info("نصيحة: تأكد من كتابة اسم الحي بشكل صحيح (مثلاً: 'الياسمين' بدلاً من 'خلف المحطة').")

        # عرض الخريطة الثابتة
        folium_static(m, width=1100, height=600)

else:
    st.info("الرجاء رفع ملف CSV يحتوي على أعمدة (الاسم، المدينة، العنوان) للبدء.")
