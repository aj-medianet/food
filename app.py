import streamlit as st
import numpy as np
import pandas as pd
import sqlite3
from pathlib import Path

st.sidebar.title('Food App')
db_file = Path("./food.sqlite")

# check sqlite DB file exists
def connect_db():
    if not db_file.is_file():
        st.write('Database does not exist')
        return False
    else:
        return sqlite3.connect(db_file)


def show_all_restaurants(cur):
    cur.execute("SELECT name FROM restaurants")
    rows = cur.fetchall()
    df = pd.DataFrame(
        rows,
        columns=["Name"]
    ) 
    st.subheader("Restaurants")
    st.table(df)


def get_restaurants(cur):
    cur.execute("SELECT name FROM restaurants")
    return cur.fetchall()


def select_restaurant(restaurants):
    return st.sidebar.selectbox('Select Restaurant', (restaurants))

def show_restaurant(cur, restaurant):
    query = "SELECT * FROM orders WHERE restaurant=\"%s\";" % (restaurant)
    cur.execute(query)
    rows = cur.fetchall()
    df = pd.DataFrame(
        rows,
        columns=[description[0] for description in cur.description]
    )
    st.table(df)

def get_cols(cur):
    cur.execute("SELECT * FROM orders")
    return [description[0] for description in cur.description]

def add_rest(cur, rest_name):
    query = "INSERT INTO restaurants VALUES(\'%s\');" % (rest_name)
    cur.execute(query)
    st.success("Successfully added {}".format(rest_name))

conn = connect_db()
if conn:
    cur = conn.cursor()

    with st.form(key="add_rest"):
        st.write("Add New Restaurant")
        rest_name = st.text_input("Restaurant Name")
        submit_button = st.form_submit_button(label='Add')

    if submit_button:
        add_rest(cur, rest_name)

    restaurants = get_restaurants(cur)
    restaurant = select_restaurant(restaurants)

    if restaurant:
        show_restaurant(cur, "".join(restaurant))

