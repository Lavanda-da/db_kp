import psycopg2
import psycopg2.extras
from settings import DB_CONFIG
import redis


REDIS_TTL = 600


r = redis.StrictRedis(
    host='localhost',
    port=6379,
    decode_responses=True
)


def publish_event(event_type, message):
    r.publish(event_type, message)


def check_user(login) -> list[dict]:
    query = """
                SELECT id 
                FROM users 
                where login = %(login)s;"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"login": login})
            return cur.fetchall()


def add_user(name, login, hash):
    query = """
            INSERT INTO users (name, login, hash_password)
            VALUES (%s, %s, %s);
        """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query,
                        (name, login, hash))
            conn.commit()


def check_supplier(login) -> list[dict]:
    query = """
                SELECT id 
                FROM suppliers 
                where login = %(login)s;"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"login": login})
            return cur.fetchall()


def add_supplier(name, adress, login, hash):
    query = """
            INSERT INTO suppliers (name, adress, login, hash_password)
            VALUES (%s, %s, %s, %s);
        """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query,
                        (name, adress, login, hash))
            conn.commit()


def get_user_id(login, password):
    redis_login = login + 'user'
    res = r.smembers(redis_login)
    res_id = -1
    checking = False
    if res != {}:
        for elem in res:
            if 'id' in elem:
                res_id = int(elem[2:])
            elif password == elem:
                checking = True
    if checking:
        publish_event('created_order', f"Создан заказ пользователем {res_id}")
        return res_id
    query = """
                SELECT id, hash_password
                FROM users 
                where login = %(login)s;
            """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"login": login})
            result = cur.fetchall()
            if result == []:
                return None
            if result[0]["hash_password"] == password:
                user_id = result[0]["id"]
                r.sadd(redis_login, password)
                r.sadd(redis_login, 'id' + str(user_id))
                r.expire(redis_login, REDIS_TTL)
                publish_event('created_order', f"Создан заказ пользователем {user_id}")
                return user_id
            return None


def get_supplier_id(login, password):
    redis_login = login + 'supplier'
    res = r.smembers(redis_login)
    res_id = -1
    checking = False
    if res != {}:
        for elem in res:
            if 'id' in elem:
                res_id = int(elem[2:])
            elif password == elem:
                checking = True
    if checking:
        publish_event('created_order', f"Создана поставка поставщиком {res_id}")
        return res_id
    query = """
                SELECT id, hash_password
                FROM suppliers 
                where login = %(login)s;
            """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"login": login})
            result = cur.fetchall()
            if result == []:
                return None
            if result[0]["hash_password"] == password:
                supplier_id = result[0]["id"]
                r.sadd(redis_login, password)
                r.sadd(redis_login, 'id' + str(supplier_id))
                r.expire(redis_login, REDIS_TTL)
                publish_event('created_order', f"Создана поставка поставщиком {supplier_id}")
                return supplier_id
            return None
