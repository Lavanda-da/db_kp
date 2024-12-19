-- Таблица для хранения информации о растениях
CREATE TABLE plants (
    id serial PRIMARY KEY,
    name varchar(512),
    height int,
    price int,
    amount int
);

COMMENT ON TABLE plants IS 'Информация о растениях';

COMMENT ON COLUMN plants.id IS 'Уникальный код растения';

COMMENT ON COLUMN plants.name IS 'Название растения';

COMMENT ON COLUMN plants.height IS 'Высота растения';

COMMENT ON COLUMN plants.price IS 'Цена растения';

COMMENT ON COLUMN plants.amount IS 'Количество растения на складе';

-- Таблица для хранения информации о поставщиках
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    login VARCHAR(50) NOT NULL,
    hash_password varchar(50) NOT NULL,
    adress varchar(200)
);

COMMENT ON TABLE suppliers IS 'Информация о поставщиках';

COMMENT ON COLUMN suppliers.id IS 'Уникальный идентификатор поставщика';

COMMENT ON COLUMN suppliers.name IS 'Имя поставщика';

COMMENT ON COLUMN suppliers.login IS 'Логин поставщика';

COMMENT ON COLUMN suppliers.hash_password IS 'Хэш пароля поставщика';

COMMENT ON COLUMN suppliers.adress IS 'Адресс поставщика';

-- Таблица для регистрации привозов растений
CREATE TABLE deliveries (
    id SERIAL PRIMARY KEY,
    supplier_id INT REFERENCES suppliers(id) ON DELETE CASCADE,
    date DATE NOT NULL
);

COMMENT ON TABLE deliveries IS 'Данные о привозах растений';

COMMENT ON COLUMN deliveries.id IS 'Уникальный идентификатор поставки';

COMMENT ON COLUMN deliveries.supplier_id IS 'Идентификатор поставщика';

COMMENT ON COLUMN deliveries.date IS 'Дата привоза';

-- Таблица для хранения состава каждой поставки
CREATE TABLE delivery_contents (
    id INT REFERENCES deliveries(id) ON DELETE CASCADE,
    plant_id int REFERENCES plants(id) ON DELETE CASCADE,
    amount INT NOT NULL
);

COMMENT ON TABLE delivery_contents IS 'Состав поставки растений';

COMMENT ON COLUMN delivery_contents.id IS 'Идентификатор поставки';

COMMENT ON COLUMN delivery_contents.plant_id IS 'Идинтификатор растения';

COMMENT ON COLUMN delivery_contents.amount IS 'Количество данного растения в поставке';

CREATE TABLE users (
    id serial PRIMARY KEY,
    name varchar(50),
    login varchar(50) not NULL,
    hash_password varchar(50) NOT NULL
);

COMMENT ON TABLE users IS 'Информация о регистрационных данных пользователя';

COMMENT ON COLUMN users.id IS 'Идентификатор пользователя';

COMMENT ON COLUMN users.name IS 'Имя пользователя';

COMMENT ON COLUMN users.login IS 'Логин пользователя';

COMMENT ON COLUMN users.hash_password IS 'Хэш пароля пользователя';

CREATE TABLE user_orders (
    id serial PRIMARY KEY,
    user_id int REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT null,
    status varchar(20) DEFAULT 'accept'
);

COMMENT ON TABLE user_orders IS 'Информация о регистрационных данных пользователя';

COMMENT ON COLUMN user_orders.id IS 'Идентификатор заказа';

COMMENT ON COLUMN user_orders.user_id IS 'Информация о пользователе, сделавшем заказ';

COMMENT ON COLUMN user_orders.date IS 'Дата создания заказа';

COMMENT ON COLUMN user_orders.status IS 'Стутас заказа отменен ли он';

CREATE TABLE orders (
    id INT REFERENCES user_orders(id) ON DELETE CASCADE,
    plant_id int REFERENCES plants(id) ON DELETE CASCADE,
    amount INT NOT NULL
);

COMMENT ON TABLE orders IS 'Информация о проданных растениях в рамках покупки';

COMMENT ON COLUMN orders.id IS 'Идентификатор покупки';

COMMENT ON COLUMN orders.plant_id IS 'Идинтификатор проданного растения';

COMMENT ON COLUMN orders.amount IS 'Количество проданного растения';

CREATE OR REPLACE FUNCTION check_plant_availability()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем, достаточно ли растений на складе
    IF NEW.amount > (SELECT amount FROM plants WHERE id = NEW.plant_id) THEN

		UPDATE user_orders
	    SET status = 'cancel'
	    WHERE id = NEW.id;

        RETURN NULL; -- Игнорируем вставку, если недостаточно растений
    END IF;

    UPDATE plants
    SET amount = amount - NEW.amount
    WHERE id = NEW.plant_id;

    RETURN NEW; -- Возвращаем новую строку, если проверки прошли успешно
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_order_availability
BEFORE INSERT ON "orders"
FOR EACH ROW
EXECUTE FUNCTION check_plant_availability();