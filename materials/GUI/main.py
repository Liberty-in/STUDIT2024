import streamlit as st
import requests
import webbrowser
from streamlit_modal import Modal
import streamlit.components.v1 as components
left, middle, right = st.columns(3)

if right.button("help", use_container_width=True):
    webbrowser.open('help.pdf')

modal = Modal("info",
    key="info",
    padding=20,
    max_width=744)

st.title("Загрузка наборов данных")
uploaded_file = st.file_uploader("Загрузите набор данных формата csv", type = 'csv')
but = st.button("Загрузить")
if but:
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        requests.post("http://127.0.0.1:5000/success", files = {'file':bytes_data})

    but2 = st.button("Предобработать данные")
    if but2:
        data = {'dataset': 'file.csv'}
        requests.post("http://127.0.0.1:5000/prepare", json = data)
        st.text("Данные предобработаны")


if middle.button("info", use_container_width=True):
    modal.open()
if modal.is_open():
    with modal.container():
        info = requests.get("http://127.0.0.1:5000/info").content
        st.write(str(info).split("'")[1])
