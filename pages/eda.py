import streamlit as st
from ui import plot_store_sales

st.title("Store Revenue")

# Checkbox filters
store_ids = []
if st.checkbox("Store 1", value=True):
    store_ids.append(1)
if st.checkbox("Store 2", value=True):
    store_ids.append(2)

if store_ids:
    fig = plot_store_sales(store_ids)  # <- returns a matplotlib figure
    st.pyplot(fig)
else:
    st.warning("Please select at least one store.")
