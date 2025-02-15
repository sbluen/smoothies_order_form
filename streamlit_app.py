# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!"""
)

name_on_smoothie = st.text_input("Name on Smoothie:")

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect("Choose up to 5 ingredients:", 
                                  my_dataframe, 
                                  max_selections=5)

ingredients_string = ""
for fruit in ingredients_list:
    ingredients_string += fruit + " "
    st.subheader(fruit + " Nutrition information")
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit)
    st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True, col("search_on"))
    st.stop()

    

my_insert_sql = """INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES (?, ?)"""

time_to_submit = st.button("Submit Order")
if time_to_submit:
    session.sql(my_insert_sql, [ingredients_string, name_on_smoothie]).collect()
    st.success("Your smoothie is ordered, %s" % name_on_smoothie, icon="✅")
    
