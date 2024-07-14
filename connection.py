import psycopg2
import os
from psycopg2 import sql
import streamlit as st

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="data",
            user="data",
            password=st.secrets["MOT"],
            host="44.211.16.14",
            port="5432"
        )

        conn.set_client_encoding('UTF8')
        
        return conn
    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        return None