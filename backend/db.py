import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

pool_config = {
    "pool_name": "restaurant_pool",
    "pool_size": 5,
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

ssl_mode = os.getenv("DB_SSL_MODE", "").strip()
ssl_ca = os.getenv("DB_SSL_CA", "").strip()

if ssl_mode:
    pool_config["ssl_disabled"] = False
    pool_config["ssl_verify_cert"] = ssl_mode.upper() in {"VERIFY_CA", "VERIFY_IDENTITY"}
    pool_config["ssl_verify_identity"] = ssl_mode.upper() == "VERIFY_IDENTITY"

if ssl_ca:
    pool_config["ssl_ca"] = ssl_ca

pool = pooling.MySQLConnectionPool(**pool_config)

def get_connection():
    return pool.get_connection()

def query(sql, params=None, fetch=True):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, params or ())
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return {"affected_rows": cursor.rowcount, "last_id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
