# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
# Write directly to the app
st.title("My parents new healthy Diner")

st.write(
    """ Choose the fruits you want in your custom Smoothie!
    """)

# new section to dispaly smoothiesfroot nutrition information


name_on_order = st.text_input('Name on Smoothies:')
st.write('the name on your smoothies will be: ',name_on_order)

cnx = st.connection("snowflake")

sessoin = cnx.session()
# now we just want to bring back the fruit name
my_fruit_list_df = sessoin.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data = my_fruit_list_df,use_container_width=True)

# convert the snowpark dataframe to a pandas dataframe 
# so we can use LOC function
ingredients_list= st.multiselect('Choose up to 5 ingredients: ', my_fruit_list_df,max_selections = 5)

pd_df = my_fruit_list_df.to_pandas()
st.dataframe(pd_df)
st.stop()




# test to know the datatype of our ingerdients variable
if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
# The += operator means "add this to what is already in the variable" so each time the FOR Loop is repeated,
# a new fruit name is appended to the existing string. 
        ingredients_string += fruit_chosen+ ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + ' Nutrition information')
    #st.write(ingredients_string)
        fruityvice_respones = requests.get("https://fruityvice.com/api/fruit/"+ search_on)
        #st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(data = fruityvice_respones.json(), use_container_width = True)
        
    # SQL insert statement
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    # st.write(my_insert_stmt)

    # adding submit button 
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        sessoin.sql(my_insert_stmt).collect()
        st.success('your smoothies is ordered,'+name_on_order,icon="✅")

