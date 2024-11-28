import streamlit as st
import requests



list_datasets = requests.get("http://127.0.0.1:5000/request_data")
data = str(list_datasets.content).split("\"")[1::2]
ch = st.radio(
    "Доступные наборы",
    data
)
bt = st.button("Выбрать")
if bt:
    st.text("Вы выбрали набор данных " + ch + " как рабочий")
    data = {'dataset': ch}
    requests.post("http://127.0.0.1:5000/setd", json=data)



