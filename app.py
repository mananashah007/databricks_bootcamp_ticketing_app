import streamlit as st

from database import run_query

st.set_page_config(
    page_title="Support Ticket System",
    page_icon="🎫",
    layout="wide",
)

st.title("🎫 Support Ticket System")
st.caption("Lakebase powered support ticket application")

# ----------------------------------------------------
# Load tickets
# ----------------------------------------------------
try:
    tickets = run_query("""
        SELECT
            ticket_id,
            title,
            status,
            created_by,
            created_at
        FROM tickets
        ORDER BY created_at DESC;
    """)
except Exception as e:
    st.error(f"Unable to connect to Lakebase.\n\n{e}")
    st.stop()

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

st.sidebar.header("Tickets")

if not tickets:
    st.warning("No tickets found.")
    st.stop()

ticket_lookup = {
    f"#{t['ticket_id']} - {t['title']}": t["ticket_id"]
    for t in tickets
}

selected_ticket = st.sidebar.selectbox(
    "Select Ticket",
    list(ticket_lookup.keys())
)

ticket_id = ticket_lookup[selected_ticket]

# ----------------------------------------------------
# Ticket Details
# ----------------------------------------------------

ticket = next(
    t for t in tickets
    if t["ticket_id"] == ticket_id
)

col1, col2 = st.columns([4,1])

with col1:
    st.subheader(ticket["title"])

with col2:
    st.metric("Status", ticket["status"])

st.write(f"**Created By:** {ticket['created_by']}")
st.write(f"**Created At:** {ticket['created_at']}")

st.divider()

# ----------------------------------------------------
# Messages
# ----------------------------------------------------

messages = run_query("""
    SELECT
        author,
        message_text,
        created_at
    FROM ticket_messages
    WHERE ticket_id=%s
    ORDER BY created_at;
""", (ticket_id,))

st.subheader("Conversation")

for message in messages:

    with st.container(border=True):

        st.write(f"**{message['author']}**")

        st.write(message["message_text"])

        st.caption(message["created_at"])
