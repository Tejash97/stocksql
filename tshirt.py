import streamlit as st
import sqlite3
import google.generativeai as genai

# Configure Genai API Key
genai.configure(api_key="AIzaSyC7lVFvGGps0cIdH2dZp3hQ3W5ARFLVe_Y")

## Function to Load Google Gemini Model and Provide Queries as Response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

## Function to Retrieve Query from the Database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

## Define Your Prompt for Retailer Focus
prompt = [
    """
    You are an expert in converting English questions to SQL queries for a retail store database. 
    The SQL database has the name 'atliq_tshirts' and has the following tables and columns:
    
    - t_shirts (t_shirt_id, brand, color, size, price, stock_quantity)
    - discounts (discount_id, t_shirt_id, pct_discount)
    
    Some example questions and their corresponding SQL queries:
    
    Example 1: "What is the stock quantity for Nike t-shirts?"
    SQL Query: SELECT SUM(stock_quantity) FROM t_shirts WHERE brand="Nike";
    
    Example 2: "What are the discounted prices for Red Adidas t-shirts?"
    SQL Query: SELECT t_shirts.brand, t_shirts.color, t_shirts.size, 
               t_shirts.price - (t_shirts.price * discounts.pct_discount / 100) AS discounted_price
               FROM t_shirts
               JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id
               WHERE t_shirts.brand="Adidas" AND t_shirts.color="Red";
    
    Example 3: "What is the total number of t-shirts available in stock?"
    SQL Query: SELECT SUM(stock_quantity) FROM t_shirts;
    
    Your job is to convert English queries like the ones above into SQL queries for the 'atliq_tshirts' database.
    The SQL code should not have any code formatting like ``` in the beginning or end.
    """
]

## Streamlit App
st.set_page_config(page_title="Retail SQL Query Generator")
st.header("English to Retail SQL Query")

# Input field for questions
question = st.text_input("Ask Your Retail Query:", key="input")

submit = st.button("Generate SQL Query")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.subheader("Generated SQL Query")
    st.write(response)
    
    # Retrieve data from the database based on the SQL query
    response_data = read_sql_query(response, "tejash_tshirts.db")
    
    st.subheader("Database Response")
    for row in response_data:
        st.write(row)
