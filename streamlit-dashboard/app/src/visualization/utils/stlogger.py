from typing import Any

# Функция для добавления в список последних действий.
def add_log(st, level: str, method: str, data: Any):
    """
    Добавление в список действий (левый sidebar) какого угодно лога.
    st - streamlit, level - уровень, method - метод, data - любые данные
    """
    
    st.session_state.actions.insert(0, {f"{level} - {method}": data})