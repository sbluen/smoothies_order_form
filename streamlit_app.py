# Import python packages
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

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)

ingredients_list = st.multiselect("Choose up to 5 ingredients:", 
                                  my_dataframe, 
                                  max_selections=5)

ingredients_string = ""
for fruit in ingredients_list:
    ingredients_string += fruit + " "
    
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0] or fruit
    st.write('The search value for ', fruit, ' is ', search_on, '.')
    
    st.subheader(fruit + " Nutrition information")
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
    #fv_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)[nutrition]
    df_smoothiefruit = pd.DataFrame(data=smoothiefroot_response.json(), use_container_width=True)[nutrition]
    st.dataframe(data=df_smoothiefruit)    #to display it

    

my_insert_sql = """INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES (?, ?)"""

time_to_submit = st.button("Submit Order")
if time_to_submit:
    session.sql(my_insert_sql, [ingredients_string, name_on_smoothie]).collect()
    st.success("Your smoothie is ordered, %s" % name_on_smoothie, icon="✅")
    
