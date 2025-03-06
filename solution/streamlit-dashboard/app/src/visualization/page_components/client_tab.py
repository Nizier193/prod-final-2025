import streamlit as st
from uuid import uuid4
import requests
from src.visualization.utils.stlogger import add_log


def client_tab(api_client):
    st.title("Создание клиента и получение рекламы")

    tab_create, tab_views_clicks = st.tabs(tabs=["Форма создания", "Получение рекламы и клики"])
    
    with tab_create:
        with st.form(key='client_form'):
            login = st.text_input(label="Логин", value="PROOOOOOOOD")
            age = st.number_input(label="Возраст", min_value=0, max_value=100, value=18)
            location = st.text_input(label="Местоположение", value="Россия")
            gender = st.selectbox(label="Пол клиента", options=["MALE", "FEMALE"])
            
            submit_button = st.form_submit_button(label='Добавить клиента')
            
            if submit_button:
                client_json = {
                    "client_id": str(uuid4()),
                    "login": login,
                    "age": age,
                    "location": location,
                    "gender": gender
                }
                
                response = api_client.create_clients_bulk([client_json])
                if response.status_code == 201:
                    st.success("Клиент успешно добавлен!")
                    st.json(response.json())
                    add_log(st, "client", "ADD", response.json())

                else:
                    st.error(f"Клиент не был добавлен. Статус: {response.status_code}")
                    add_log(st, "client", "ERROR", response.status_code)

                    if response.text:
                        st.error(f"Ошибка: {response.text}")


    with tab_views_clicks:
        st.text("Получение рекламы и клики.")

        clientId = st.text_input(
            label="Введите clientId для работы получения рекламы.", 
            key="user_ad_input"
        )
        adId = st.text_input(
            label="Введите ID рекламы, только для клика!", 
            key="user_click_input"
        )

        if st.button("Получить рекламу"):
            status: requests.Response = api_client.get_ad(clientId=clientId)

            if status.status_code == 200:
                st.success("Реклама успешно получена")

                ad_json = status.json()
                st.json(ad_json)
                add_log(st, "ads", "GET", ad_json)

            else:
                st.error(f"Ошибка получения рекламы. {status.status_code}")
                add_log(st, "ads", "ERROR", status.status_code)


        if st.button("Сымитировать нажатие на рекламу"):
            status: requests.Response = api_client.make_click(adId=adId, clientId=clientId)

            if status.status_code == 204:
                st.success(f"Клик зафиксирован. {status.status_code}")
                add_log(st, "click", "ADD", status.status_code)

            elif status.status_code == 200:
                st.warning(f"Этот пользователь уже кликал на это объявление. {status.status_code}")
                add_log(st, "click", "STOP", status.status_code)
            
            else:
                st.error(f"Ошибка нажатия на рекламу. {status.status_code}")
                add_log(st, "click", "ERROR", status.status_code)

