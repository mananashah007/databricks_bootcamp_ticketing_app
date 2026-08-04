import streamlit as st
from database import Database

st.set_page_config(
    page_title="Support Ticket System",
    layout="wide"
)

st.title("Welcome to Support Ticket System")

try:

    db = Database()

    tickets = db.get_all_tickets()

    st.success("Connected to Lakebase!")

    st.dataframe(
        tickets,
        use_container_width=True
    )

except Exception as e:

    st.error(str(e))
