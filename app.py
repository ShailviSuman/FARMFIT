import streamlit as st
import pandas as pd
import joblib
import requests

# Load model
model = joblib.load("fertilizer_model.pkl")

import json

with open("lang.json", "r", encoding="utf-8") as f:
    translations = json.load(f)
