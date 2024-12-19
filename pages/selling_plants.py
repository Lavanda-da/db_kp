import pandas as pd
from datetime import datetime
import streamlit as st

import repositories.plants
import repositories.register
import repositories.hash_func


# Хранение добавленных товаров в таблице
if "plants_table" not in st.session_state:
    st.session_state.plants_table = pd.DataFrame(
        columns=["Название", "Высота", "Цена", "Количество"]
    )


@st.cache_data
def get_plants() -> dict[str, str]:
    plants = repositories.plants.get_plants()
    res = {}
    for plant in plants:
        count = 2
        while plant["name"] in res.keys():
            if plant["name"] + str(count) not in res.keys():
                plant["name"] += str(count)
            else:
                count += 1
        res[plant["name"]] = [plant["id"], plant["height"], plant["price"]]

    return res


def add_plant_event(plant_name,  plant_height, plant_price, plant_quantity):
    new_row = pd.DataFrame(
        {
            "Название": [plant_name],
            "Высота": [plant_height],
            "Цена": [plant_price],
            "Количество": [plant_quantity],
        }
    )
    st.session_state.plants_table = pd.concat(
        [st.session_state.plants_table, new_row], ignore_index=True
    )


def clear_table_event():
    st.session_state.plants_table = pd.DataFrame(
        columns=["Название", "Высота", "Цена", "Количество"]
    )


def get_user_id(login, password):
    user_id = repositories.register.get_user_id(login, repositories.hash_func.hash(password))
    return user_id


def add_user_order(user_id, order_info):
    date = datetime.now().date()
    order_id = repositories.orders.add_user_order(user_id, date)["id"]
    unsuccess = []
    for index, row in order_info.iterrows():
        plant_info = repositories.plants.get_plant_by_all_info(row["Название"], row["Цена"], row["Высота"])
        plant_id = plant_info[0]["id"]
        result = repositories.orders.add_order_detail(order_id, plant_id, row["Количество"])
        if result == None:
            unsuccess += [index]
    return unsuccess


plants = get_plants()


def show_selling_plants_page():
    st.title("Для покупателей")

    # Поля для ввода данных
    st.write("Введите данные")
    login_user = st.text_input("Логин пользователя")
    password_user = st.text_input("Пароль пользователя")
    selected_plant= st.selectbox("Выберите растение", plants.keys())
    quantity = st.number_input("Количество", min_value=1, max_value=100, value=1)

    # кнопки
    add_plant_btn = st.button("Добавить растение")
    clear_table_btn = st.button("Очистить таблицу")
    apply_btn = st.button("Подтвердить продажу")

    # event handlers
    if add_plant_btn:
        add_plant_event(selected_plant,
                        plants[selected_plant][1],
                        plants[selected_plant][2],
                        quantity)

    if clear_table_btn:
        clear_table_event()

    if apply_btn and len(st.session_state.plants_table) > 0:
        user_id = get_user_id(login_user, password_user)
        if user_id != None:
            result = add_user_order(user_id, st.session_state.plants_table)
            if result == []:
                st.success(f"Продажа добавлена успешно!")
            else:
                output = "На складе недостаточно растений, следующие заказы не сформированы: " + ' '.join(map(str, result))
                st.error(output)
            clear_table_event()
        else:
            st.error(f"Неправильный логин или пароль")
    elif apply_btn:
        st.error(f"Необходимо заполнить корзину")

    st.write("Добавленные товары:")
    st.dataframe(st.session_state.plants_table)
