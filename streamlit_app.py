import logging
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!"""
)

name_on_smoothie = st.text_input("Name on Smoothie:")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect("Choose up to 5 ingredients:",
                                  my_dataframe,
                                  max_selections=5)

ingredients_string = ""
for fruit in ingredients_list:
    ingredients_string += fruit + " "

    search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0] or fruit

    st.subheader(fruit + " Nutrition information")
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
    try:
        fetched_df = pd.DataFrame(smoothiefroot_response.json())
        #Now it comes in 7 columns and we only want the nutrient name and amount
        fetched_df = pd.DataFrame(fetched_df['nutrition'].items(), columns=['nutrient', 'amount'])
        st.dataframe(data=fetched_df, use_container_width=True, hide_index=True)
    except ValueError:
        st.write("bad keyword? " + search_on)
        st.write("This data is currrently unavailable.")

my_insert_sql = """INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES (?, ?)"""

time_to_submit = st.button("Submit Order")
if time_to_submit:
    session.sql(my_insert_sql, [ingredients_string, name_on_smoothie]).collect()
    st.success("Your smoothie is ordered, %s" % name_on_smoothie, icon="✅")
