import os
from lakebase import run_query, run_write

tickets_table = os.environ.get("tickets","tickets")
ticket_messages_table = os.environ.get("ticket_messages","ticket_messages")

def get_all_tickets():
    return run_query(f"""
        SELECT
            ticket_id,
            title,
            status,
            created_by,
            created_at
        FROM {tickets_table}
        ORDER BY created_at DESC;
    """)


def get_ticket_messages(ticket_id):
    return run_query(f"""
        SELECT
            author,
            message_text,
            created_at
        FROM {ticket_messages_table}
        WHERE ticket_id = %s
        ORDER BY created_at;
    """, (ticket_id,))


def create_ticket(title, created_by):

    run_write(f"""
        INSERT INTO {tickets_table}(title,status,created_by)
        VALUES(%s,'open',%s)
    """,(title,created_by))


def add_message(ticket_id,message,author):

    run_write(f"""
        INSERT INTO {ticket_messages_table}(ticket_id,message_text,author)
        VALUES(%s,%s,%s)
    """,(ticket_id,message,author))


def update_ticket_status(ticket_id,status):

    run_write(f"""
        UPDATE {tickets_table}
        SET status=%s
        WHERE ticket_id=%s
    """,(status,ticket_id))