# mongo/client.py

from pymongo import MongoClient as PyMongoClient
from pymongo.errors import ConnectionFailure

from infrastructure.config.settings import MongoDBSettings


class MongoClient:
    def __init__(self, settings: MongoDBSettings | None = None):
        self.settings = settings or MongoDBSettings()
        self.client = PyMongoClient(
            self.settings.uri,
            serverSelectionTimeoutMS=5000
        )

        self.database = self.client.get_database(self.settings.database)

    def connect(self):
        """
        Verify MongoDB connection.
        """
        try:
            self.client.admin.command("ping")
            print("MongoDB connected")
        except ConnectionFailure as e:
            raise Exception(
                f"MongoDB connection failed: {e}"
            )

    def get_database(self):
        """
        Return current database instance.
        """
        return self.database

    def close(self):
        """
        Close Mongo connection.
        """
        self.client.close()


mongo_client = MongoClient()


def get_database():
    return mongo_client.get_database()
