from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st

db_connection_string = st.secrets["SUPABASE_CONNECTION_STRING"]

load_dotenv()

'''
def get_supabase_data_df(sql_query):
    """
    Fetch data from Supabase PostgreSQL Sakila database
    
    Args:
        sql_query (str): SQL query to execute
        
    Returns:
        tuple: (sql_query, dataframe) - The executed query and resulting pandas DataFrame
        
    Example:
        query = "SELECT * FROM film LIMIT 10"
        sql, df = get_supabase_data_df(query)
    """
    try:
        # Try to get full connection string first, then fallback to individual components
        supabase_connection_string = os.getenv("SUPABASE_CONNECTION_STRING")
        
        if supabase_connection_string:
            # Use the full connection string directly from Supabase
            connection_string = supabase_connection_string
        else:
            # Fallback to building from components
            supabase_url = os.getenv("SUPABASE_DB_URL")
            supabase_password = os.getenv("SUPABASE_DB_PASSWORD")
            
            if not supabase_url or not supabase_password:
                raise ValueError("Missing Supabase credentials. Please check your .env file.")
            
            # Create PostgreSQL connection string for Supabase
            # Format: postgresql://postgres:[password]@[host]:[port]/postgres
            connection_string = f"postgresql://postgres:{supabase_password}@{supabase_url}"
        
        # Create SQL engine
        engine = create_engine(connection_string)
        
        # Execute query and create dataframe
        with engine.connect() as connection:
            sql_query_obj = text(sql_query)
            result = connection.execute(sql_query_obj)
            
            # Get column names from the result
            column_names = result.keys()
            
            # Fetch all results
            rows = result.fetchall()
            
            # Create DataFrame with proper column names
            df = pd.DataFrame(rows, columns=column_names)
            
            return  df # sql_query
            
    except Exception as e:
        #st.error(f"Database connection error: {str(e)}")
        raise RuntimeError(f"Database connection error: {str(e)}")

        #return pd.DataFrame()  # sql_query,  Return empty DataFrame on error
'''    


def get_supabase_data_df(sql_query):
    """
    Fetch data from Supabase PostgreSQL Sakila database
    
    Args:
        sql_query (str): SQL query to execute
        
    Returns:
        tuple: (sql_query, dataframe) - The executed query and resulting pandas DataFrame
        
    Example:
        query = "SELECT * FROM film LIMIT 10"
        sql, df = get_supabase_data_df(query)
    """
    try:
        # Try to get full connection string first, then fallback to individual components
        engine = create_engine(db_connection_string)
         
        # Execute query and create dataframe
        with engine.connect() as connection:
            sql_query_obj = text(sql_query)
            result = connection.execute(sql_query_obj)
            
            # Get column names from the result
            column_names = result.keys()
            
            # Fetch all results
            rows = result.fetchall()
            
            # Create DataFrame with proper column names
            df = pd.DataFrame(rows, columns=column_names)
            
            return  df # sql_query
            
    except Exception as e:
        raise RuntimeError(f"Database connection error: {str(e)}")


def retrieve_data_from_sql(query: str) -> pd.DataFrame:
    
    env_path = Path.cwd() / ".env"

    load_dotenv(dotenv_path=env_path)

    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

    df = pd.read_sql(query, engine)

    df.head()

    return df

# MySQL local DB
def get_store_sales() -> pd.DataFrame:
    query_daily_store_sales = """
        SELECT 
        DATE(r.rental_date) as rental_day,
        i.store_id,
        sum(p.amount) as revenue
        from rental r 
        JOIN inventory i 
        ON i.inventory_id = r.inventory_id
        JOIN payment p
        ON p.rental_id = r.rental_id
        WHERE r.rental_date < '2006-01-01'
        group by rental_day, i.store_id
        ORDER BY rental_day;"""
    df = retrieve_data_from_sql(query_daily_store_sales)
    return df

# Supabase PostgreSQL DB
def get_store_sales_postgree() -> pd.DataFrame:
    query_daily_store_sales = """
        SELECT 
        DATE(r.rental_date) AS rental_day,
        i.store_id,
        SUM(p.amount) AS revenue
        FROM rental r
        JOIN inventory i 
        ON i.inventory_id = r.inventory_id
        JOIN payment p
        ON p.rental_id = r.rental_id
        WHERE r.rental_date < '2006-01-01'
        GROUP BY DATE(r.rental_date), i.store_id
        ORDER BY DATE(r.rental_date);
        """
    df = get_supabase_data_df(query_daily_store_sales)
    return df