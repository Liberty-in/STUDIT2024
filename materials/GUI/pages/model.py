import streamlit as st
import requests


list_datasets = requests.get("http://127.0.0.1:5000/request_model")
data = str(list_datasets.content).split("\"")[1::2]
ch = st.radio(
    "Доступные модели",
    data
)

bt = st.button("Выбрать")
if bt:
    st.text("Вы выбрали модель " + ch + " как рабочую")
    data = {'model': ch}
    requests.post("http://127.0.0.1:5000/setm", json=data)