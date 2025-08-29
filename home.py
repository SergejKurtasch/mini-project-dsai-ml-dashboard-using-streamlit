import streamlit as st

def main():
    st.title("Home")
    st.divider()
    st.header("Film Recommendation System")
    st.write("Some description")
    st.divider()

    st.subheader("Store Revenue Dashboard")
    st.write("View store revenue trends on a separate page.")

    # Link to the chart page – works because eda.py is in /pages
    st.page_link(
        "pages/eda.py",
        label="EDA Page",
    )

if __name__ == "__main__":
    main()
