import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

st.set_page_config(page_title="Food App")
st.title('Food App')

db_file = Path("./food.sqlite")
conn = sqlite3.connect(db_file)


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
    return st.selectbox('Select Restaurant', (restaurants))


def show_restaurant(cur, restaurant):
    query = "SELECT * FROM orders WHERE restaurant=\"%s\";" % (restaurant)
    cur.execute(query)
    rows = cur.fetchall()
    df = pd.DataFrame(
        rows,
        columns=[description[0] for description in cur.description]
    )
    st.table(df)


def add_rest(cur, rest_name):
    query = "INSERT INTO restaurants VALUES(\'%s\');" % (rest_name)
    cur.execute(query)
    conn.commit()
    st.success("Successfully added {}".format(rest_name))


def del_rest(cur, rest_name):
    query = "DELETE FROM restaurants WHERE name=\'%s\'" % (rest_name)
    cur.execute(query)
    conn.commit()
    st.success("Successfully deleted {}".format(rest_name))


def add_order(cur, rest_name, dish, rating):
    st.write(rest_name, dish, rating)
    name = ''.join(rest_name)
    cur.execute("INSERT INTO orders(restaurant, dish, rating) VALUES(?, ?, ?)",(name, dish, rating))
    conn.commit()
    st.success("Successfully Added {}".format(dish))

def get_dishes(cur, rest_name):
    query = "SELECT dish FROM orders where restaurant=\'%s\'" % rest_name
    st.write(query)
    cur.execute(query)
    return cur.fetchall()

def delete_order(cur, rest_name, dish):
    rest = ''.join(rest_name)
    d = ''.join(dish)
    query = "DELETE FROM orders WHERE restaurant=\'%s\' AND dish=\'%s\'" % (rest, d)
    cur.execute(query)
    conn.commit()
    st.success("Deleted {} from {}".format(d, rest))


if conn:
    cur = conn.cursor()
    restaurants = get_restaurants(cur)
    
    menu = ["Home", "Add Order", "Delete Order", "Add Restaurant", "Delete Restaurant", "Download Database"]
    choice = st.selectbox("", menu)

    if choice == 'Home':
        restaurant = select_restaurant(restaurants)
        if restaurant:  
            show_restaurant(cur, "".join(restaurant))
    
    elif choice == "Add Order":
        # add order form
        with st.form(key="add_order"):
            rest_name = st.selectbox("Restaurant Name", restaurants)
            dish = st.text_input("Dish")
            rating = st.text_input("Rating")
            submit_add_order = st.form_submit_button(label='Add Order')

        if submit_add_order:
            add_order(cur, rest_name, dish, rating)

    elif choice == "Delete Order":
        # delete order form
        with st.form(key="delete_order"):
            rest_name = st.selectbox("Restaurant Name", restaurants)
            dishes = get_dishes(cur, rest_name)
            dish = st.selectbox("Dish", dishes)
            submit_delete_order = st.form_submit_button(label='Delete Order')

        if submit_delete_order:
            delete_order(cur, rest_name, dish)
    
    elif choice == "Add Restaurant":
        # add rest form
        with st.form(key="add_rest"):
            st.write("Add New Restaurant")
            add_rest_name = st.text_input("Restaurant Name")
            submit_add = st.form_submit_button(label='Add')

        if submit_add:
            add_rest(cur, add_rest_name)
        
    elif choice == "Delete Restaurant": 
        # delete rest form
        with st.form(key='delete_rest'):
            del_rest_name = st.selectbox('Select Restaurant to Delete', restaurants)
            submit_delete = st.form_submit_button(label="Delete")

        if submit_delete:
            del_rest(cur, del_rest_name)

    elif choice == "Download Database":
        with open(db_file, "rb") as fp:
            btn = st.download_button(
                label="Download Database",
                data=fp,
                file_name="food.sqlite",
                mime="application/octet-stream"
            )
    

