from uuid import uuid4
import streamlit as st

from src.visualization.utils.stlogger import add_log


def advertisers_tab(api_client):
    st.title("Создание рекламодателя")

    with st.form(key='advertiser_form'):
        name = st.text_input(label="Название рекламодателя", placeholder="Введите название")
        submit_button = st.form_submit_button(label='Добавить рекламодателя')
        
        if submit_button:
            if not name:
                st.error("Пожалуйста, введите название рекламодателя")
                return
                
            advertiser = {
                "advertiser_id": str(uuid4()),
                "name": name
            }
            
            response = api_client.create_advertisers_bulk([advertiser])
            if response.status_code == 201:
                st.success("Рекламодатель был успешно зарегистрирован!")
                st.json(response.json())
                add_log(st, "advertiser", "ADD", response.json())
            else:
                st.error(f"Рекламодатель не был зарегистрирован. Статус: {response.status_code}")
                add_log(st, "advertiser", "ERROR", response.status_code)
