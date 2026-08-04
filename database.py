import os
import pandas as pd
from sqlalchemy import create_engine


class Database:

    def __init__(self):

        host = os.environ["PGHOST"]
        port = os.environ["PGPORT"]
        database = os.environ["PGDATABASE"]
        user = os.environ["PGUSER"]
        password = os.environ["PGPASSWORD"]

        connection_string = (
            f"postgresql+psycopg://{user}:{password}"
            f"@{host}:{port}/{database}"
        )

        self.engine = create_engine(connection_string)

    def get_all_tickets(self):

        query = """
            SELECT *
            FROM tickets
            ORDER BY created_at DESC
        """

        return pd.read_sql(query, self.engine)
