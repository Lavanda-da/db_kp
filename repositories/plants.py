import psycopg2
import psycopg2.extras
from settings import DB_CONFIG


def get_plants() -> list[dict]:
    query = """SELECT id, name, height, price 
               FROM plants
               WHERE amount > 0;"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()


def get_plant_by_all_info(name, price, height):
    query = """
            SELECT id, amount
            FROM plants
            WHERE
                name = %(name)s and
                height = %(height)s and
                price = %(price)s
            GROUP BY id, name, height, price;
        """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"name": name,
                                "height": height,
                                "price": price})
            return cur.fetchall()


def add_new_plant(name, price, height, amount):
    query = """
                INSERT INTO plants (name, price, height, amount)
                VALUES (%(name)s, %(price)s, %(height)s, %(amount)s) RETURNING id;
            """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query,
                        {"name": name,
                         "price": price,
                         "height": height,
                         "amount": amount})
            return cur.fetchone()


def update_plant_amount(plant_id, amount):
    query = """
                UPDATE plants 
                SET amount = (%(amount)s)
                WHERE id = (%(id)s);
            """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query,
                        {"amount": amount,
                         "id": plant_id})
            conn.commit()
