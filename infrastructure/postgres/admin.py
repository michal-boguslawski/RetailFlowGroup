from sqlalchemy import text
from sqlalchemy.engine import Engine

from infrastructure.postgres.models import Base


class PostgresAdminClient:
    def __init__(self, engine: Engine):
        self.engine = engine

    def truncate_tables(self):
        with self.engine.begin() as conn:
            conn.execute(
                text("""
                    TRUNCATE TABLE
                        order_items,
                        orders,
                        users,
                        products
                    RESTART IDENTITY CASCADE
                """)
            )

    def reset_schema(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
