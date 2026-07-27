from sqlalchemy import text
from sqlalchemy.engine import Engine

from infrastructure.postgres.models import Base, MetadataBase


class PostgresAdminClient:
    def __init__(self, engine: Engine, store: str = "alpha"):
        self.engine = engine
        self.store = store
        self.metadata = Base.metadata if store == "alpha" else MetadataBase.metadata

    def truncate_tables(self):
        table_names = [table.name for table in self.metadata.sorted_tables]
        if not table_names:
            return

        tables_sql = ", ".join(table_names)

        with self.engine.begin() as conn:
            conn.execute(
                text(f"TRUNCATE TABLE {tables_sql} RESTART IDENTITY CASCADE")
            )

    def reset_schema(self):
        self.metadata.drop_all(self.engine)
        self.metadata.create_all(self.engine)
