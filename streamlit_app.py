# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("Customize your Smoothie :balloon:")
st.write(
    """
    Choose the fruits you want in your custom Smoothie
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

session = get_active_session()
df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=df, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose uo to 5 ingredients:', 
    df, 
    max_selections=5
)


ingredients_string = ''
if len(ingredients_list)>0:
    for fruit_choosen in ingredients_list:
        ingredients_string+=fruit_choosen+" "

    st.write(ingredients_string)
    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order) values('""" + ingredients_string + """', '"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    
if ingredients_string:
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered, "+name_on_order, icon="✅")
