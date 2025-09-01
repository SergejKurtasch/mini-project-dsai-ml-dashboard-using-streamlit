import streamlit as st

def main():
    st.image("pages/img.png", use_container_width=True)

    st.divider()

    st.page_link(
        "pages/eda.py",
        label="EDA Page",
    )

    st.page_link(
        "pages/predictions.py",
        label="Predictions Page",
    )

if __name__ == "__main__":
    main()
