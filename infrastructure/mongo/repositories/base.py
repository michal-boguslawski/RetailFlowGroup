from pymongo.database import Database
from pymongo.collection import Collection


class BaseRepository:

    def __init__(self, database: Database, collection_name: str):
        self.database: Database = database
        self.collection_name: str = collection_name
        self.collection: Collection = self.database.get_collection(collection_name)

    def find_by_id(self, id_: str, *args, **kwargs):
        return self.collection.find_one({"_id": id_})

    def upsert(self, record: dict) -> None:
        result = self.collection.insert_one(record)
        # print(result.acknowledged)

    def bulk_upsert(self, records: list[dict]) -> None:
        result = self.collection.insert_many(records)
        # print(result.acknowledged)

    def find_random(self, *args, **kwargs):
        cursor = self.collection.aggregate([
            {"$sample": {"size": 1}}
        ])

        result = cursor.to_list(length=1)
        return result[0] if result else None
