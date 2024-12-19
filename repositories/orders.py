import psycopg2
import psycopg2.extras
from settings import DB_CONFIG


def add_supplier_delivery(supplier_id, date):
    query = """
                INSERT INTO deliveries (supplier_id, date)
                VALUES (%(supplier_id)s, %(date)s) RETURNING id;
            """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query,
                        {"supplier_id": supplier_id,
                         "date": date})
            return cur.fetchone()


def add_user_order(user_id, date):
    query = """
                INSERT INTO user_orders (user_id, date)
                VALUES (%(id)s, %(date)s) RETURNING id;
            """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query,
                        {"id": user_id,
                         "date": date})
            return cur.fetchone()


def add_delivery_detail(delivery_id, plant_id, amount):
    query = """
                INSERT INTO delivery_contents (id, plant_id, amount)
                VALUES (%(id)s, %(plant_id)s, %(amount)s);
            """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query,
                        {"id": delivery_id,
                         "plant_id": plant_id,
                         "amount": amount})
            conn.commit()


def add_order_detail(order_id, plant_id, amount):
    query = """
                INSERT INTO orders (id, plant_id, amount)
                VALUES (%(id)s, %(plant_id)s, %(amount)s) RETURNING id;
            """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query,
                        {"id": order_id,
                         "plant_id": plant_id,
                         "amount": amount})
            return cur.fetchone()