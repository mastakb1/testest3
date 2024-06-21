import mysql.connector
import pandas as pd
from dbConfig import read_config

def create_connection():
    config = read_config()
    return mysql.connector.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )


def get_data_from_db(query):
    conn = create_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
