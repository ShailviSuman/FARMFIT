import streamlit as st
import pandas as pd
import joblib
import requests
import json

# Load model
model = joblib.load("farmfit_model.pkl")

# Load translations
with open("lang.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

# Language selection
lang = st.selectbox("🌐 Language / மொழி / भाषा", list(translations.keys()))
t = translations[lang]

# Title
st.title(t["title"])

# Inputs
crop = st.selectbox(t["crop"], ["Rice", "Wheat", "Millets", "Cotton", "Sugarcane"])
soil = st.selectbox(t["soil"], ["Clay", "Loam", "Sandy", "Black"])
pH = st.number_input(t["soil_ph"], min_value=4.5, max_value=9.0, step=0.1)
city = st.text_input(t["rainfall"])  # Rainfall input via city

# Get rainfall using weather API
def get_rainfall(city):
    try:
        api_key = "d78e0c7f2f4e12ed453d76c416a84718"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()
        rainfall = res.get("rain", {}).get("1h", 0)
        return rainfall
    except:
        return 75  # fallback

# Submit and predict
if st.button(t["submit"]):
    if not crop or not soil or not city:
        st.error(t["errors"]["missing_input"])
    elif pH < 4.5 or pH > 9.0:
        st.warning(t["errors"]["invalid_pH"])
    else:
        rainfall = get_rainfall(city)
        input_df = pd.DataFrame([{
            "Crop": crop,
            "Soil_Type": soil,
            "Rainfall_mm": rainfall,
            "Soil_pH": pH
        }])
        prediction = model.predict(input_df)[0]
        compost, n, p, k = map(lambda x: round(x, 2), prediction)

        st.subheader(t["output"])
        st.markdown(f"🌿 **Compost**: {compost} kg/acre")
        st.markdown(f"🧪 **NPK**: {n}:{p}:{k} kg/acre")
