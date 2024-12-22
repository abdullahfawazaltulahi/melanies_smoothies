# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title("My parents new healthy Diner")

st.write(
    """ Choose the fruits you want in your custom Smoothie!
    """)
# # interactive selectBox
# fruit_option = st.selectbox('What is your Favorite Fruit?',
#                            ('Banana','Strawberries','Peaches'))
# st.write('your Favorite Fruits is : ',fruit_option)

# option = st.selectbox('How would you liwk to be contacted?',('-','Email','Home Phonbe','Mobile Number'))
# st.write('you selected: ',option)
# new section to dispaly smoothiesfroot nutrition information


name_on_order = st.text_input('Name on Smoothies:')
st.write('the name on your smoothies will be: ',name_on_order)
cnx = st.connection("snowflake")
sessoin = cnx.session()
# now we just want to bring back the fruit name
my_fruit_list_df = sessoin.table('SMOOTHIES.PUBLIC.FRUIT_OPTIONS').select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data = my_fruit_list_df,use_container_width=True)
st.stop()

ingredients_list= st.multiselect(
    'Choose up to 5 ingredients: ',
    my_fruit_list_df,max_selections = 5)
# test to know the datatype of our ingerdients variable
if ingredients_list:
#    st.write(ingredients_lst)
#    st.text(ingredients_lst)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
# The += operator means "add this to what is already in the variable" so each time the FOR Loop is repeated,
# a new fruit name is appended to the existing string. 
        ingredients_string += fruit_chosen+ ' '
        st.subheader(fruit_chosen + ' Nutrition information')
    #st.write(ingredients_string)
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_chosen)
        #st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
    # SQL insert statement
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    # st.write(my_insert_stmt)

    # adding submit button 
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        sessoin.sql(my_insert_stmt).collect()
        st.success('your smoothies is ordered,'+name_on_order,icon="✅")


