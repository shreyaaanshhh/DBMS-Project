import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

pool = pooling.MySQLConnectionPool(
    pool_name="restaurant_pool",
    pool_size=5,
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 14491)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"), 
)

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
