# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!"""
)

name_on_smoothie = st.text_input("Name on Smoothie:")

csx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect("Choose up to 5 ingredients:", 
                                  my_dataframe, 
                                  max_selections=5)

ingredients_string = ""
for fruit in ingredients_list:
    ingredients_string += fruit + " "

my_insert_sql = """INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES (?, ?)"""

time_to_submit = st.button("Submit Order")
if time_to_submit:
    session.sql(my_insert_sql, [ingredients_string, name_on_smoothie]).collect()
    st.success("Your smoothie is ordered, %s" % name_on_smoothie, icon="✅")
