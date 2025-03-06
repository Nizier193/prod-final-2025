import streamlit as st

from core.config import config
from src.api.data_retrieve_service import DataRetrieveService
from src.models.constants import Mode

from src.visualization.page_components.metric_render import create_entity_tab

service = DataRetrieveService(config)

def initialize_session_data(
        n_clients: int,
        n_advertisers: int,
        n_campaigns_per_advertiser: int,
        max_impressions: int,
        max_clicks: int
    ):
    """Заполняет сервер тестовыми данными для графиков."""
    st.session_state.campaign_data, st.session_state.clients_data = service.insert_some_data(
        n_clients,
        n_advertisers,
        n_campaigns_per_advertiser,
        max_impressions,
        max_clicks
    )
    st.success("Test data inserted successfully!")



def analytics_page():
    """Страница с аналитикой."""
    st.title("📊 PROD - Аналитический дашборд.")

    with st.sidebar:
        with st.expander(label="Ячейка для генерации тестовых данных"):
            st.info("При повторной генерации данных, БД не удаляется! Учитывайте это при анализе метрик =) ")

            n_clients = st.slider(label="Количество клиентов", min_value=1, max_value=5000, value=200)
            n_advertisets = st.slider(label="Количество рекламодателей", min_value=1, max_value=10, value=1)
            n_campaigns_per_advertiser = st.slider(label="Количество кампаний у рекламодателя", min_value=1, max_value=10, value=1)
            max_impressions = st.slider(label="Максимально количество просмотров рекламы", min_value=1, max_value=10000, value=500)
            max_clicks = st.slider(label="Максимальное количество кликов по рекламе", min_value=1, max_value=10000, value=500)

            st.text("Каждый раз генерировать данные не нужно - после генерации нажмите на 'Обновить отображение датафрейма.'")
            if st.button("Сгенерировать тестовые данные"):
                with st.spinner("Идёт добавление данных"):
                    initialize_session_data(
                        n_clients, 
                        n_advertisets, 
                        n_campaigns_per_advertiser,
                        max_impressions,
                        max_clicks
                    )
                
            st.text("Тестовые данные")
            if st.button("Обновить отображение датафрейма"):
                data = st.session_state.campaign_data
                if len(data) == 0:
                    st.info("Вы ещё не сгенерировали данные.")
                else:
                    st.text("Датафрейм рекламодатель - кампания")
                    st.dataframe(st.session_state.campaign_data)
                    st.text("Датафрейм с юзерами")
                    st.dataframe(st.session_state.clients_data)

        with st.expander("Список последних действий"):
            st.text("Здесь выводится список последних действий (создание, удаление, своеобразный буфер обмена)")
            st.button(label="Обновление списка", help="Если не отображается, можно нажать перезагрузить =)")
            st.json(st.session_state.actions, expanded=False)

    current_mode = st.selectbox(
        label="Режим отображения:",
        options=[mode.value for mode in Mode],
        format_func=lambda x: "По дням" if x == Mode.DAILY.value else "Агрегированный"
    )
    st.session_state.selector = current_mode

    # Main tabs
    advertiser_tab, campaign_tab = st.tabs([
        "📊 Статистика по рекламодателю (AdvertiserId)",
        "📈 Статистика по кампании (CampaignId)",
    ])

    with campaign_tab:
        st.subheader("Аналитика кампании")
        create_entity_tab(
            entity_type="кампании",
            get_daily_func=service.get_campaign_stat_daily,
            get_aggregate_func=service.get_campaign_stat,
            input_key="campaign_input"
        )

    with advertiser_tab:
        st.subheader("Аналитика рекламодателя")
        create_entity_tab(
            entity_type="рекламодателя",
            get_daily_func=service.get_advertiser_stat_daily,
            get_aggregate_func=service.get_advertiser_stat,
            input_key="advertiser_input"
        )