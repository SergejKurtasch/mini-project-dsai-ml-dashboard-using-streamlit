from pathlib import Path
from sqlalchemy import create_engine, text
import os
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

db_connection_string = st.secrets["SUPABASE_CONNECTION_STRING"]


@st.cache_data
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



# Supabase PostgreSQL DB
@st.cache_data
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


@st.cache_data
def get_total_store_sales() -> pd.DataFrame:
    query_total_store_sales = """
        SELECT 
        store_id,
        SUM(amount) AS revenue
        FROM rental
        JOIN inventory USING (inventory_id)
        JOIN payment USING (rental_id)
        WHERE rental_date < '2006-01-01'
        GROUP BY store_id
        ORDER BY store_id;
    """
    df = get_supabase_data_df(query_total_store_sales)
    return df


@st.cache_data
def get_top5_rented_films() -> pd.DataFrame:
    query_top5_rented_films = """
        WITH ranked AS (
            SELECT 
                i.store_id,
                f.title,
                COUNT(r.rental_id) AS rental_count,
                ROW_NUMBER() OVER (
                    PARTITION BY i.store_id
                    ORDER BY COUNT(r.rental_id) DESC
                ) AS rating
            FROM rental r
            JOIN inventory i USING (inventory_id)
            JOIN film f USING (film_id)
            WHERE EXTRACT(YEAR FROM r.rental_date) = 2005
            GROUP BY i.store_id, f.title
        )
        SELECT store_id, title
        FROM ranked
        WHERE rating <= 5
        ORDER BY store_id, rating
        ;
        """
    df = get_supabase_data_df(query_top5_rented_films)
    
    return df


@st.cache_data
def get_film_descriptions() -> pd.DataFrame:
    query_film_descriptions = """
        SELECT 
        film_id,
        title,
        description
        FROM film;
        """
    df = get_supabase_data_df(query_film_descriptions)
    return df


@st.cache_data
def get_doc_embeddings(_model, df):
    return _model.encode(df["description"].tolist())


def semantic_search(model, query, documents, descriptions, doc_embeddings, top_n=5):
    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:top_n]
    results = [
        (documents[idx], descriptions[idx], similarities[idx])
        for idx in top_indices
    ]
    return results