import streamlit as st
import requests
import re

import pandas as pd
import numpy as np

#data = {'index': 'feature_1'}
#requests.post("http://127.0.0.1:5000/column", json=data)
ch = st.radio(
    "Доступные признаки:",
    ["feature_1", "feature_2", "feature_3"]
)
bt = st.button("Выбрать")
if bt:
    predicts = requests.get("http://127.0.0.1:5000/predict")
    x = requests.get("http://127.0.0.1:5000/column").content
    pr = str(predicts.content).split("\\n")[1:-2]
    ap = []
    for i in range(len(pr)):
        ap.append(re.findall(r"\d+", pr[i])[0])
    t = str(x).split("\\n")[1:-2]
    apt = []
    for i in range(len(t)):
        apt.append(re.findall(r"\d+", t[i])[0] + "." + re.findall(r"\d+", t[i])[1])
    chart_data = pd.DataFrame(ap, apt)
    st.line_chart(chart_data)
