import requests
import streamlit as st
from src.visualization.utils.stlogger import add_log


def campaigns_tab(api_client):
    st.title("Создание новой рекламной кампании")
    st.text("Страничка создания кампании, внизу страницы загрузка фото")

    tab_create, tab_images, tab_text_generate = st.tabs(tabs=["Создание кампании", "Добавление картинок", "Генерация текста"])
    
    with tab_create:
        st.subheader("Форма создания")
        
        with st.form(key='campaign_form'):
            advertiser_id = st.text_input(label="ID рекламодателя", placeholder="Введите advertiser_id")
            
            # Основные параметры кампании
            ad_title = st.text_input(label="Заголовок рекламы", placeholder="Введите заголовок")
            ad_text = st.text_input(label="Текст рекламы", placeholder="Введите рекламный текст")
            
            col1, col2 = st.columns(2)
            with col1:
                impressions_limit = st.number_input(label="Лимит показов", min_value=0, value=1000)
                cost_per_impression = st.number_input(label="Стоимость за показ", min_value=0.0, value=0.1)
                start_date = st.number_input(label="Дата начала", min_value=0, value=1)
            
            with col2:
                clicks_limit = st.number_input(label="Лимит кликов", min_value=0, value=100)
                cost_per_click = st.number_input(label="Стоимость за клик", min_value=0.0, value=1.0)
                end_date = st.number_input(label="Дата окончания", min_value=0, value=30)

            # Настройки таргетинга
            st.subheader("Настройки таргетинга")
            gender = st.selectbox(label="Пол", options=["MALE", "FEMALE", "ALL"])
            age_from = st.number_input(label="Возраст от", min_value=0, max_value=100, value=1)
            age_to = st.number_input(label="Возраст до", min_value=0, max_value=100, value=30)
            location = st.text_input(label="Локация", value="Россия")
            
            targeting = {
                "gender": gender,
                "age_from": age_from,
                "age_to": age_to,
                "location": location
            }

            submit_button = st.form_submit_button(label='Создать кампанию')
            
            if submit_button:
                if not advertiser_id or not ad_title or not ad_text:
                    st.error("Пожалуйста, заполните все обязательные поля")
                    return
                    
                campaign = {
                    "advertiser_id": advertiser_id,
                    "impressions_limit": impressions_limit,
                    "clicks_limit": clicks_limit,
                    "cost_per_impression": cost_per_impression,
                    "cost_per_click": cost_per_click,
                    "ad_title": ad_title,
                    "ad_text": ad_text,
                    "start_date": start_date,
                    "end_date": end_date,
                    "targeting": targeting
                }
                
                response = api_client.create_campaign(advertiserId=advertiser_id, campaign=campaign)
                
                if response.status_code == 201:
                    st.success("Кампания была успешно создана!")
                    campaign_json = response.json()
                    st.json(campaign_json)
                    
                    if "*" in (campaign_json.get("ad_text", "") + campaign_json.get("ad_title", "")):
                        st.warning("Обратите внимание, что ваша кампания не проходит модерацию.")
                    
                    add_log(st, "campaigns", "ADD", campaign_json)
                        
                elif response.status_code == 400:
                    st.error("Кампания не была создана, ошибка валидации.")
                    error_json = response.json()
                    st.json(error_json)

                    add_log(st, "campaigns", "ERROR", error_json)
                    
                else:
                    st.error(f"Кампания не была создана. Статус: {response.status_code}")
                    
                    add_log(st, "campaigns", "ERROR", response.status_code)


    with tab_images:
        st.subheader("Управление картинками кампаний.")

        campaignId = st.text_input(label="campaignId, которой нужно добавить картинки")
        
        # Добавляем загрузчик файлов
        uploaded_file = st.file_uploader(
            "Выберите изображение", 
            type=['png', 'jpg', 'jpeg']
        )

        if st.button("Отправить фото") and uploaded_file is not None:
            # uploaded_file уже является файлоподобным объектом, который можно использовать как open()
            response = api_client.add_photo(campaignId=campaignId, image=uploaded_file)

            if response.status_code == 201:
                st.success("Фотография успешно прикреплена к кампании.")
                st.json(response.json())
            else:
                st.error("Картинку не удалось загрузить")
                st.json(response.content)

        if st.button("Получить фото"):
            response = api_client.get_photos(campaignId=campaignId)

            if response.status_code == 200:
                st.success("Картинки были успешно получены.")
                st.json(response.json())
            else:
                st.error("Картинки не удалось получить.")
                st.json(response.content)

    with tab_text_generate:
        st.subheader("Генерация текста к кампании")
        st.info("Сгенерированный текст автоматически заменяется на тот, что был сгенерирован.")

        prompt = st.text_input(
            label="Промпт к генерации текста", 
            value="Супер красивый текст",
            key="prompt_input"
        )
        advertiser_id = st.text_input(
            label="ID Рекламодателя", 
            value="abcdefgh", 
            key="adv_input"
        )
        campaign_id = st.text_input(
            label="ID кампании", 
            value="abcdefgh", 
            key="camp_input"
        )

        if st.button(label="Начать генерацию"):
            with st.spinner(text="Генерируем..."):
                status = api_client.generate_text(
                    prompt=prompt,
                    advertiserId=advertiser_id,
                    campaignId=campaign_id
                )

                if status.status_code == 200:
                    st.success("Текст сгенерирован успешно!")
                    st.json(status.json())

                else:
                    st.error(f"Текст не удалось сгенерировать -> {status.status_code}")