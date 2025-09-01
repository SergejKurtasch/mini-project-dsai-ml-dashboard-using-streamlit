import streamlit as st
from ui import plot_daily_store_sales, format_top5, plot_total_store_sales
from backend import get_top5_rented_films

col1, col2, col3 = st.columns([4,7,4])
with col2:
    st.title("Store Revenue")

st.markdown("---")

col1, col2, col3 = st.columns([4,7,4])
with col2:
    st.subheader("Total Revenue by Store")


fig2 = plot_total_store_sales()
st.pyplot(fig2)


st.markdown("---")

col1, col2, col3 = st.columns([4,7,4])
with col2:
    st.subheader("Daily Revenue by Store")

col_l, col1, col2, col_r = st.columns([3, 1, 1, 3])

store_ids = []
with col1:
    if st.checkbox("Store 1", value=True):
        store_ids.append(1)
with col2:
    if st.checkbox("Store 2", value=True):
        store_ids.append(2)

if store_ids:
    
    fig = plot_daily_store_sales(store_ids)
    st.pyplot(fig)

    df_top5 = get_top5_rented_films()

    st.markdown("---")

    col1, col2, col3 = st.columns([2,8,2])
    with col2:
        st.subheader("Top 5 Rented Films by Store in 2005")

    if len(store_ids) == 2:
        col_left, col_right = st.columns(2)

        with col_left:
            sid = store_ids[0]
            st.markdown(f"Store {sid}")
            st.dataframe(format_top5(df_top5, sid), use_container_width=True)

        with col_right:
            sid = store_ids[1]
            st.markdown(f"Store {sid}")
            st.dataframe(format_top5(df_top5, sid), use_container_width=True)

    else:
        sid = store_ids[0]
        st.markdown(f"Store {sid}")
        st.dataframe(format_top5(df_top5, sid), use_container_width=True)

else:
    st.warning("Please select at least one store.")
