# 🌾 FarmFit – Adaptive Fertilizer Recommendation Based on Weather

A solo-developed ML + Web project under the **Hack4Nature 1.0** hackathon (Rural Innovation Track).

---

## 🌍 Project Overview

**FarmFit** is a smart, personalized fertilizer recommendation system designed for rural farmers in India. It uses machine learning to suggest optimal compost and NPK fertilizer quantities based on:

* **Soil pH**
* **Crop type**
* **Soil texture**
* **Local rainfall**

The system prioritizes **economically feasible**, **eco-friendly**, and **regionally realistic** solutions.

---

## ⚙️ Features

* Predicts **Compost (kg/acre)** and **NPK (kg/acre)** for 5 key Indian crops
* Inputs: Soil pH, Crop, Soil Type, Rainfall (mm)
* Outputs: Adaptive and cost-efficient fertilizer dosages
* Adjusts recommendations based on **soil type and rainfall impact**
* Supports **vernacular PDFs** for low-literacy, rural accessibility
* Built using **Streamlit** for a fast and friendly UI

---

## 📊 Dataset: fertilizer\_data.csv

The dataset contains 60 handcrafted rows with the following columns:

| Feature                | Description                                   |
| ---------------------- | --------------------------------------------- |
| Soil\_pH               | Range: 5.5–7.5 depending on crop requirements |
| Crop                   | Rice, Wheat, Millets, Cotton, Sugarcane       |
| Soil\_Type             | Clay, Loam, Sandy, Black                      |
| Rainfall\_mm           | 30–200 mm across Low, Medium, High bands      |
| Compost\_kg\_per\_acre | Adjusted based on crop and soil type          |
| NPK\_kg\_per\_acre     | Adjusted based on rainfall and crop needs     |

---

## 🤝 Adjustment Logic & Scientific Basis

### 🌧️ Rainfall-Based NPK Adjustment

* **High rainfall (121–200 mm)**: NPK increased \~10%
* **Low rainfall (30–59 mm)**: NPK reduced \~10%
* **Why?**

  * Nitrogen leaches in high rainfall; more is needed
  * Low rainfall = risk of over-fertilization

### 🌱 Soil-Type-Based Compost Adjustment

* **Sandy soil**: Compost increased by \~10%
* **Why?**

  * Sandy soils lack water/nutrient retention

> ✍️ **All recommendations align with ICAR and FAO agronomic practices.**

---

## 🔍 Data Sources and Citations

* [ICAR Soil and Nutrient Management PDF](https://icar.org.in/sites/default/files/inline-files/NRM-2702.pdf)
* [ICAR Crop Management Handbook](https://icar.org.in/sites/default/files/inline-files/Crop_Management.pdf)
* [FAO Fertilizer Use in India](https://www.fao.org/3/y5460e/y5460e0e.htm)
* [PennState: Nitrogen Efficiency vs Rainfall](https://extension.psu.edu/nutrient-management-to-improve-nitrogen-efficiency-and-reduce-environmental-loss)
* [Oregon State: Soil Types and Organic Matter](https://news.oregonstate.edu/news/adding-organic-matter-improves-garden-soils)

---

## 🚀 Tech Stack

* **Streamlit** – Web interface
* **Python (scikit-learn)** – Model training and deployment
* **Pandas / joblib** – Data preprocessing and model saving

---

## 🙌 How to Run

1. Clone the repo
2. Run `pip install -r requirements.txt`
3. Run `streamlit run app.py`

---

## 🌟 Why It Stands Out

* Grounded in real agronomic logic (not random ML!)
* Localized and accessible for Indian rural farmers
* Solo-built, with no prebuilt AI tools or templates
* Uses adaptive fertilizer logic backed by ICAR & FAO
* Fully working prototype + transparent methodology

---

## 🧑‍💻 CREATED By

**Team Hackure** – Solo participant
**Name:** - **SHAILVI SUMAN**
**Email:** - **23f2002671@ds.study.iitm.ac.in**
