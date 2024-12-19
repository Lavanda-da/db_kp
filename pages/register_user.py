import streamlit as st

import repositories.register
import repositories.hash_func


def check(login):
    if repositories.register.check_user(login) == []:
        return True
    return False


def add_user(name, login, password):
    if check(login):
        repositories.register.add_user(name, login, repositories.hash_func.hash(password))
        return True
    return False

def show_register_user_page():
    st.title("Регистрация пользователя")

    # Поля для ввода данных
    name_user_log = st.text_input("Введите Ваше имя")
    login_user_log = st.text_input("Придумайте логин пользователя")
    password_user_log = st.text_input("Придумайте пароль ")

    # кнопки
    register_user_btn = st.button("Зарегистрироваться")

    # event handlers
    if register_user_btn:
        if add_user(name_user_log, login_user_log, password_user_log):
            st.success(f"Регистрация прошла успешно!")
        else:
            st.error(f"Пользователь с таким логином уже существует")

