import streamlit as st
import pandas as pd

from src.visualization.analytic_page import analytics_page
from src.visualization.data_page import data_page
from src.visualization.info_page import info_page 

st.set_page_config(layout="centered")

if ("campaign_data" not in st.session_state) or ("clients_data" not in st.session_state):
    st.session_state.campaign_data = pd.DataFrame() # Пустой датафрейм
    st.session_state.clients_data = pd.DataFrame() # Пустой датафрейм

if ("banwords" not in st.session_state):
    st.session_state.banwords = pd.DataFrame()

if ("actions" not in st.session_state):
    st.session_state.actions = []

# Структура проекта по страницам.
page1, page2, page3 = st.tabs(["Страница аналитики", "Добавление данных", "Информация / Инструкция"])
with page1:
    analytics_page()

with page2:
    data_page()

with page3:
    info_page()