import streamlit as st
import pandas as pd

def moderation_tab(api_client):
    st.title("Управление модерацией")

    with st.expander("Список запрещенных слов (очень опасно)"):
        if st.button("Обновить список запрещённых слов."):
            banwords = api_client.moderation_get_banwords().json()
            st.session_state.banwords = pd.DataFrame(banwords)

        st.dataframe(st.session_state.banwords)

    with st.container(border=True):
        new_banword = st.text_input(label="Добавить новое бан-слово", key="banwords_input")

        if st.button("Добавить слово"):
            status = api_client.moderation_add_banwords(new_banword)
            if status.status_code == 201:
                st.success("Банворд добавлен!")
            else:
                st.error(f"Банворд не был добавлен: {status.json().get("error")}")


    moderation_activity = st.selectbox(label="Выключить или включить модерацию.", options=["Включить", "Выключить"])
    strict_moderation = st.selectbox(label="Строгая или нестрогая модерация.", options=["Нестрогая", "Строгая"])

    st.text("Нестрогая модерация заменяет плохие слова на *, строгая возвращает 400.")

    if st.button("Применить настройки к модерации"):
        api_client.moderation_switch(status=(moderation_activity == "Включить"))
        api_client.moderation_strict(status=(strict_moderation == "Строгая"))

        with st.container():
            st.info(f"Статус модерации: {moderation_activity}")
            st.info(f"Статус строгости: {strict_moderation}")