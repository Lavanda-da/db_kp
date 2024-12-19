import streamlit as st

import repositories.register
import repositories.hash_func


def check(login):
    if repositories.register.check_supplier(login) == []:
        return True
    return False


def add_supplier(name, adress, login, password):
    if check(login):
        repositories.register.add_supplier(name, adress, login, repositories.hash_func.hash(password))
        return True
    return False

def show_register_supplier_page():
    st.title("Регистрация поставщика")

    # Поля для ввода данных
    name_supplier_log = st.text_input("Введите название компании")
    adress_supplier_log = st.text_input("Введите адрес")
    login_supplier_log = st.text_input("Придумайте логин поставщика")
    password_supplier_log = st.text_input("Придумайте пароль")

    # кнопки
    register_supplier_btn = st.button("Зарегистрироваться")

    # event handlers
    if register_supplier_btn:
        if add_supplier(name_supplier_log, adress_supplier_log, login_supplier_log, password_supplier_log):
            st.success(f"Регистрация прошла успешно!")
        else:
            st.error(f"Поставщик с таким логином уже существует")
