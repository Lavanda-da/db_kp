from pages.selling_plants import show_selling_plants_page
import streamlit as st
from pages.delivery_plants import show_delivery_plants_page
from pages.register_user import show_register_user_page
from pages.register_supplier import show_register_supplier_page


# Главная логика приложения с навигацией
def main():
    st.sidebar.title("Навигация")
    page = st.sidebar.radio(
        "Перейти к странице",
        ["Для покупателей", "Для поставщиков", "Регистрация пользователя", "Регистрация поставщика"],
    )
    if page == "Для покупателей":
        show_selling_plants_page()
    elif page == "Для поставщиков":
        show_delivery_plants_page()
    elif page == "Регистрация пользователя":
        show_register_user_page()
    elif page == "Регистрация поставщика":
        show_register_supplier_page()



if __name__ == "__main__":
    main()
