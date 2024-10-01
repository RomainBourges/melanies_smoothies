# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("Customize your Smoothie")
st.write(
    """
    Choose the fruits you want in your custom Smoothie
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON))
pd_df = df.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    'Choose uo to 5 ingredients:', 
    df, 
    max_selections=5
)

ingredients_string = ''
if len(ingredients_list)>0:
    for fruit_choosen in ingredients_list:
        ingredients_string+=fruit_choosen+" "
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choosen)
        jsonDf = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    st.write(ingredients_string)
    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order) values('""" + ingredients_string + """', '"""+name_on_order+"""')"""
    
if ingredients_string:
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered, "+name_on_order, icon="✅")
