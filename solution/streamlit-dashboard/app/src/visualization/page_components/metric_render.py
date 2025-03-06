import streamlit as st
import plotly.express as px
import pandas as pd

from src.models.constants import Mode, METRIC_COLUMNS, DATE_SLIDER_HELP

def render_metrics(stats, is_aggregate=False):
    # Отображение ключевых данных. Показывает выше графиков.
    cols = st.columns(METRIC_COLUMNS)
    metric_data = {
        "Всего показов": stats['impressions_count'].sum() if not is_aggregate else stats['impressions_count'],
        "Всего кликов": stats['clicks_count'].sum() if not is_aggregate else stats['clicks_count'],
        "Средняя конверсия": f"{stats['conversion'].mean():.1f}%" if not is_aggregate else f"{stats['conversion']:.1f}%",
        "Общие затраты": f"${stats['spent_total'].sum():.2f}" if not is_aggregate else f"${stats['spent_total']:.2f}"
    }
    
    for (col, (title, value)) in zip(cols, metric_data.items()):
        col.metric(title, value)

def render_plots(stats):
    # Отображение графиков.
    graphs, conversion, payments = st.tabs(["Показы и клики", "Конверсия", "Затраты"])
    
    with graphs:
        fig = px.line(stats, x='date', y=['impressions_count', 'clicks_count'],
                      title='Показы и клики по дням',
                      labels={'value': 'Количество', 'date': 'День', 'variable': 'Метрика'})
        st.plotly_chart(fig, use_container_width=True)

    with conversion:
        fig = px.line(stats, x='date', y='conversion',
                      title='Конверсия по дням',
                      labels={'conversion': 'Конверсия (%)', 'date': 'День'})
        st.plotly_chart(fig, use_container_width=True)

    with payments:
        fig = px.area(stats, x='date', y=['spent_impressions', 'spent_clicks', 'spent_total'],
                      title='Затраты по дням',
                      labels={'value': 'Сумма', 'date': 'День', 'variable': 'Тип затрат'})
        st.plotly_chart(fig, use_container_width=True)

        total_spent = pd.DataFrame({
            'Категория': ['Показы', 'Клики'],
            'Сумма': [stats['spent_impressions'].sum(), stats['spent_clicks'].sum()]
        })
        fig_pie = px.pie(total_spent, values='Сумма', names='Категория', title='Распределение затрат')
        st.plotly_chart(fig_pie, use_container_width=True)

def handle_daily_stats(get_data_func, entity_id, key_suffix):
    # Обработка дневных статистик
    stats = get_data_func(entity_id)
    if stats is None:
        st.error("Статистика не найдена.")
        return

    st.success(f"Найдена статистика за {len(stats)} дней")
    min_day, max_day = 1, len(stats)

    if min_day != max_day:
        left, right = st.slider(
            'Выбрать диапазон дней:',
            min_value=min_day,
            max_value=max_day,
            value=(min_day, max_day),
            help=DATE_SLIDER_HELP,
            key=f"slider_{key_suffix}"
        )
    else:
        left, right = (min_day, min_day)

    if st.button("Получить статистику", key=f"btn_{key_suffix}"):
        filtered_stats = stats[(stats.date >= left) & (stats.date <= right)]
        st.dataframe(filtered_stats)
        render_metrics(filtered_stats)
        render_plots(filtered_stats)

def handle_aggregate_stats(get_data_func, entity_id):
    # Обработка агрегированных статистик.
    stats = get_data_func(entity_id)
    if stats is None:
        st.error("Статистика не найдена.")
        return

    st.success("Агрегированная статистика")
    st.dataframe(stats)
    render_metrics(stats, is_aggregate=True)

def create_entity_tab(entity_type, get_daily_func, get_aggregate_func, input_key):
    # Инпуты под клиентов и рекламодателей.
    entity_id = st.text_input(f"Введите {entity_type} ID:", key=input_key)
    if not entity_id:
        return

    if st.session_state.selector == Mode.DAILY.value:
        handle_daily_stats(get_daily_func, entity_id, input_key)
    else:
        handle_aggregate_stats(get_aggregate_func, entity_id)
