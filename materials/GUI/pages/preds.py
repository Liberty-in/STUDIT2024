import streamlit as st
import requests
import re

predicts = requests.get("http://127.0.0.1:5000/predict")
j = predicts.content
pr = str(j).split("\\n")[1:-2]
ap = []

for i in range(len(pr)):
    ap.append(re.findall(r"\d+", pr[i])[0])
st.text(ap)
