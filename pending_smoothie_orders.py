import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

session = get_active_session()

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write("Orders that need to be filled.")

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()


if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button("Submit")
    if submitted:
        try:
            st.success("Someone clicked the button.", icon='👍')
            og_dataset = session.table("smoothies.public.orders")
            edited_dataset = session.create_dataframe(editable_df)
            og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.success("Order(s) updated!", icon='👍')
        except Exception as e:
            st.write("Error: %s" % e)

else:
    st.success("There are no pending orders right now", icon='👍')
