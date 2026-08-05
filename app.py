import streamlit as st
import os
from databricks.sdk import WorkspaceClient

from services import (
    get_all_tickets,
    get_ticket_messages,
    create_ticket,
    add_message,
    update_ticket_status
)

# ----------------------------------------------------
# Page Config
# ----------------------------------------------------

st.set_page_config(
    page_title="Support Ticket System",
    page_icon="🎫",
    layout="wide"
)

st.title("🎫 Support Ticket System")
st.caption("Powered by Databricks Apps + Lakebase")

# ----------------------------------------------------
# Load Tickets
# ----------------------------------------------------

try:
    tickets = get_all_tickets()

except Exception as e:
    st.error(f"Unable to load tickets.\n\n{e}")
    st.stop()

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.title("🎫 Support Tickets")

# ---------- Create Ticket ----------

st.sidebar.markdown("## ➕ Create Ticket")

with st.sidebar.form("create_ticket_form"):

    new_title = st.text_input("Title")

    new_creator = st.text_input("Created By")

    submitted = st.form_submit_button("Create Ticket")

    if submitted:

        if not new_title or not new_creator:
            st.sidebar.error("Please fill all fields.")

        else:

            create_ticket(new_title, new_creator)

            st.sidebar.success("Ticket Created!")

            st.rerun()

st.sidebar.divider()

# ---------- Ticket Selection ----------

if not tickets:

    st.warning("No tickets available.")

    st.stop()

ticket_lookup = {
    f"#{ticket['ticket_id']} - {ticket['title']}": ticket["ticket_id"]
    for ticket in tickets
}

selected_ticket = st.sidebar.selectbox(
    "Select Ticket",
    list(ticket_lookup.keys())
)

ticket_id = ticket_lookup[selected_ticket]

ticket = next(
    t for t in tickets
    if t["ticket_id"] == ticket_id
)

# ----------------------------------------------------
# MAIN PAGE
# ----------------------------------------------------

col1, col2 = st.columns([4,1])

with col1:

    st.subheader(ticket["title"])

    st.write(f"**Created By:** {ticket['created_by']}")

    st.write(f"**Created At:** {ticket['created_at']}")

with col2:

    st.metric("Status", ticket["status"])

st.divider()

# ----------------------------------------------------
# Conversation
# ----------------------------------------------------

messages = get_ticket_messages(ticket_id)

st.subheader("💬 Conversation")

if not messages:

    st.info("No messages available.")

else:

    for message in messages:

        with st.container(border=True):

            st.write(f"**{message['author']}**")

            st.write(message["message_text"])

            st.caption(message["created_at"])

# ----------------------------------------------------
# Add Message
# ----------------------------------------------------

st.divider()

st.subheader("➕ Add Message")

with st.form("add_message_form"):

    author = st.text_input("Author")

    message = st.text_area("Message")

    submit_message = st.form_submit_button("Add Message")

    if submit_message:

        if not author or not message:

            st.error("Please complete all fields.")

        else:

            add_message(ticket_id, message, author)

            st.success("Message Added!")

            st.rerun()

# ----------------------------------------------------
# Update Status
# ----------------------------------------------------

st.divider()

st.subheader("🔄 Update Ticket Status")

status_options = [
    "open",
    "in_progress",
    "resolved"
]

current_status_index = status_options.index(ticket["status"])

with st.form("status_form"):

    new_status = st.selectbox(
        "Status",
        status_options,
        index=current_status_index
    )

    submit_status = st.form_submit_button("Update Status")

    if submit_status:

        update_ticket_status(ticket_id, new_status)

        st.success("Status Updated!")

        st.rerun()