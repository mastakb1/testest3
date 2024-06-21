import streamlit as st
import os
import toml

# Fungsi untuk membaca konfigurasi
def read_config():
    config = {}
    
    # Coba membaca dari file config.toml jika ada
    if os.path.exists('config.toml'):
        config = toml.load('config.toml')['database']
    elif st.secrets:
        # Jika tidak ada file config.toml, gunakan secrets Streamlit jika tersedia
        config = {
            'host': st.secrets["host"],
            'port': st.secrets["port"],
            'user': st.secrets["user"],
            'password': st.secrets["password"],
            'database': st.secrets["database"]
        }
    else:
        # Jika tidak ada file config.toml dan tidak ada secrets Streamlit, gunakan default
        config = {
            'host': os.getenv('DB_HOST', 'kubela.id'),
            'port': int(os.getenv('DB_PORT', '3306')),
            'user': os.getenv('DB_USER', 'davis2024irwan'),
            'password': os.getenv('DB_PASSWORD', 'wh451n9m@ch1n3'),
            'database': os.getenv('DB_DATABASE', 'aw')
        }
    
    return config