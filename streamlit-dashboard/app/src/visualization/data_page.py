from uuid import uuid4
import streamlit as st
import pandas as pd

from core.config import config
from src.api.data_registry_service import APIRegistryClient
from src.visualization.utils.stlogger import add_log

# page components
from src.visualization.page_components.client_tab import client_tab
from src.visualization.page_components.moderation_tab import moderation_tab
from src.visualization.page_components.advertisers_tab import advertisers_tab
from src.visualization.page_components.campaigns_tab import campaigns_tab

api_client = APIRegistryClient(
    base_url=(config.BACKEND_BASEURL)
    .rstrip("/")
)

def data_page():
    st.title("📊 PROD - Дашборд для заполнения данными.")

    clients, advertisers, campaigns, moderation, time = st.tabs(
        [
            "Добавление клиентов", 
            "Добавление рекламодателей", 
            "Добавление кампаний", 
            "Управление модерацией",
            "Управление временем"
        ]
    )

    with clients:
        client_tab(api_client)

    with campaigns:
        campaigns_tab(api_client)

    with advertisers:
        advertisers_tab(api_client)

    with moderation:
        moderation_tab(api_client)

    with time:
        with st.container(border=True):
            if st.button("Получить текущую дату"):
                add_log(st, "time", "GET", api_client.get_time())

                st.text(f"Текущая дата: {api_client.get_time()}")

            time_value = st.number_input(
                label="Установка текущего дня", 
                min_value=1,
            )

            if st.button("Установить время"):
                status = api_client.set_time(time_value)
                add_log(st, "time", "SET", status.json().get("current_date"))

                if status.status_code == 200:
                    st.success(f"Время успешно установлено на {time_value} день.")