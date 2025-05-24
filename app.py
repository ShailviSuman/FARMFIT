import streamlit as st
import pandas as pd
import joblib
import requests
import json
import altair as alt  # Import at the top

# --- CSS for fonts and button styles ---
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-size: 18px !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1 { font-size: 36px !important; font-weight: 700; }
    h2 { font-size: 28px !important; font-weight: 600; }
    h3 { font-size: 22px !important; font-weight: 500; }
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load model and translations
model = joblib.load("farmfit_model.pkl")

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
city = st.text_input(t["City"], placeholder="e.g., Chennai, Mumbai, Delhi")



# Function to get rainfall from API
def get_rainfall(city):
    if not city:
        return 0  # No city entered, no rainfall
    api_key = "d78e0c7f2f4e12ed453d76c416a84718"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        rain_1h = data.get("rain", {}).get("1h", None)
        rain_3h = data.get("rain", {}).get("3h", None)

        if rain_1h is not None:
            return rain_1h
        elif rain_3h is not None:
            return rain_3h / 3
        else:
            return 0
    except requests.exceptions.HTTPError:
        st.error("City not found or API error. Please enter a valid city.")
        return None
    except Exception as e:
        st.error(f"Error fetching rainfall data: {e}")
        return None

# Button and prediction logic
if st.button(t["submit"]):
    if not crop or not soil or not city:
        st.error(t["errors"]["missing_input"])
    elif pH < 4.5 or pH > 9.0:
        st.warning(t["errors"]["invalid_pH"])
    else:
        rainfall = get_rainfall(city)
        if rainfall is None:
            st.stop()  # Stop if API failed

        st.write(f"🌧️ Estimated Rainfall: {rainfall} mm")

        # Show rainfall bar chart
        rain_data = pd.DataFrame({
            "Type": ["Rainfall (mm)"],
            "Value": [rainfall]
        })
        chart = alt.Chart(rain_data).mark_bar(color="skyblue").encode(
            x='Type',
            y='Value'
        ).properties(width=300, height=200)
        st.altair_chart(chart)

        # Prepare input for model
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
