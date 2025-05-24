import streamlit as st
import pandas as pd
import joblib
import requests
import json
import altair as alt  
import plotly.express as px


# CSS for fonts and button styles 
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


model = joblib.load("farmfit_model.pkl")

with open("lang.json", "r", encoding="utf-8") as f:
    translations = json.load(f)


lang = st.selectbox("🌐 Language / மொழி / भाषा", list(translations.keys()))
t = translations[lang]


st.title(t["title"])

# Inputs
crop = st.selectbox(t["crop"], ["Rice", "Wheat", "Millets", "Cotton", "Sugarcane"])
soil = st.selectbox(t["soil"], ["Clay", "Loam", "Sandy", "Black"])
pH = st.number_input(t["soil_ph"], min_value=4.5, max_value=9.0, step=0.1)
city = st.text_input(t["rainfall"], placeholder="Name your city to get rainfall e.g., Chennai, Mumbai, Delhi")


def get_rainfall(city):
    api_key = "d78e0c7f2f4e12ed453d76c416a84718"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        # Sum up rainfall for today (first 8 time blocks of 3h = 24h)
        rainfall = 0
        for i in range(8):
            rain_val = data["list"][i].get("rain", {}).get("3h", 0)
            rainfall += rain_val

        return round(rainfall, 2)

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
            st.stop()
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

        
        input_df = pd.DataFrame([{
            "Crop": crop,
            "Soil_Type": soil,
            "Rainfall_mm": rainfall,
            "Soil_pH": pH
        }])


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

        # ✅ Now comes the visualizations
        st.subheader("📊 Visualizations")

        # 1. Rainfall Bar Plot
        rain_data = pd.DataFrame({
            "Parameter": ["Rainfall (mm)"],
            "Value": [rainfall]
        })

        rain_chart = alt.Chart(rain_data).mark_bar(color="skyblue").encode(
            x=alt.X("Parameter", title=""),
            y=alt.Y("Value", title="Millimetres (mm)")
        ).properties(width=300, height=200)

        st.altair_chart(rain_chart)

        # 2. NPK Composition Pie Chart
        npk_data = pd.DataFrame({
            "Nutrient": ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"],
            "Value": [n, p, k]
        })

        fig = px.pie(npk_data, names="Nutrient", values="Value", title="🔬 NPK Composition")
        st.plotly_chart(fig)

        # 3. Compost & Nutrient Summary Bar Chart
        summary_data = pd.DataFrame({
            "Type": ["Compost", "N", "P", "K"],
            "Value (kg/acre)": [compost, n, p, k]
        })

        summary_chart = alt.Chart(summary_data).mark_bar(color="mediumseagreen").encode(
            x="Type",
            y="Value (kg/acre)"
        ).properties(width=400, height=250)

        st.altair_chart(summary_chart)

