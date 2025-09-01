import streamlit as st
from backend import get_film_descriptions, get_doc_embeddings, semantic_search
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from textwrap import fill


st.title("Film Recommendation System")


user_input = st.text_area("Input film's description", height=150, value = "An insightful story about a boy and his dog who must redeem a young man in Australia.")

if st.button("Get Recommendations") and user_input.strip():
    df_films = get_film_descriptions()

    model = SentenceTransformer('all-MiniLM-L6-v2')
    doc_embeddings = get_doc_embeddings(model, df_films)

    results = semantic_search(
        model=model,
        query=user_input,
        documents=df_films["title"].tolist(),
        descriptions=df_films["description"].tolist(),
        doc_embeddings=doc_embeddings,
        top_n=3
    )

    st.divider()
    df_results = pd.DataFrame(results, columns=["Title", "Description", "Similarity"])
    df_results.index = df_results.index + 1
    df_results.index.name = "#"

    st.subheader("Top 3 Recommended Films")
    df_display = df_results.copy()
    df_display["Similarity"] = (df_display["Similarity"] * 100).round(1).astype(str) + "%"


    df_display["Description"] = df_display["Description"].apply(lambda s: fill(str(s), width=75))

    st.table(df_display) 



