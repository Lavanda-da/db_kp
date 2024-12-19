import pandas as pd
from datetime import datetime
import streamlit as st

import repositories.register
import repositories.hash_func
import repositories.orders
import repositories.plants

if "delivery_table" not in st.session_state:
    st.session_state.delivery_table = pd.DataFrame(
        columns=["Название", "Цена", "Высота", "Количество"]
    )


def add_plant_event(plant_name, plant_price, plant_height, plant_quantity):
    new_row = pd.DataFrame(
        {
            "Название": [plant_name],
            "Цена": plant_price,
            "Высота": plant_height,
            "Количество": [plant_quantity],
        }
    )
    st.session_state.delivery_table = pd.concat(
        [st.session_state.delivery_table, new_row], ignore_index=True
    )


def clear_table_event():
    st.session_state.delivery_table = pd.DataFrame(
        columns=["Название", "Цена", "Высота", "Количество"]
    )


def get_supplier_id(login, password):
    supplier_id = repositories.register.get_supplier_id(login, repositories.hash_func.hash(password))
    return supplier_id


def add_delivery(supplier_id, delivery_info):
    date = datetime.now().date()
    delivery_id = repositories.orders.add_supplier_delivery(supplier_id, date)["id"]
    for index, row in delivery_info.iterrows():
        plant_info = repositories.plants.get_plant_by_all_info(row["Название"], row["Цена"], row["Высота"])
        plant_id = -1
        if plant_info == []:
            plant_id = repositories.plants.add_new_plant(row["Название"], row["Цена"], row["Высота"], row["Количество"])["id"]
        else:
            plant_id = plant_info[0]["id"]
            repositories.plants.update_plant_amount(plant_info[0]["id"], plant_info[0]["amount"] + int(row["Количество"]))
        repositories.orders.add_delivery_detail(delivery_id, plant_id, row["Количество"])


def show_delivery_plants_page():
    st.title("Для поставщиков")

    # Поля для ввода данных
    st.write("Введите данные")
    login_supplier = st.text_input("Логин поставщика")
    password_supplier = st.text_input("Пароль поставщика")
    name = st.text_input("Название растения")
    price = st.number_input("Цена", min_value=1, step=1, format="%d")
    height = st.number_input("Высота", min_value=1, step=1, format="%d")
    quantity = st.number_input("Количество", min_value=1, step=1, format="%d")

    # кнопки
    add_plant_btn = st.button("Добавить растение")
    clear_table_btn = st.button("Очистить таблицу")
    apply_btn = st.button("Подтвердить поставку")

    # event handlers
    if add_plant_btn:
        add_plant_event(name, price, height, quantity)

    if clear_table_btn:
        clear_table_event()

    if apply_btn and len(st.session_state.delivery_table) > 0:
        supplier_id = get_supplier_id(login_supplier, password_supplier)
        if supplier_id != None:
            add_delivery(supplier_id, st.session_state.delivery_table)
            st.success(f"Поставка добавлена успешно!")
            clear_table_event()
        else:
            st.error(f"Неверный логин или пароль")
    elif apply_btn:
        st.error(f"Необходимо заполнить корзину")

    st.write("Добавленные товары:")
    st.dataframe(st.session_state.delivery_table)
