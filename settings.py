import os
# from dotenv import load_dotenv
#
# load_dotenv("env.env")

# Чтение и установка env
DB_CONFIG = {
    "dbname": "mydatabase",
    "user": "myuser",
    "password": "mypassword",
    "host": "localhost",
    "port": 5432,
}

# Pool settings
POOL_MIN_CONN = 1
POOL_MAX_CONN = 10
