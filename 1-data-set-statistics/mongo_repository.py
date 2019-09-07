from typing import List, Dict
from pymongo import MongoClient
from pymongo.database import Database


class MongoRepository:

    def __init__(self, server_host: str, port: str, data_base: str):
        self.__client = MongoClient(f"mongodb://{server_host}:{port}/")
        self.__database: Database = self.__client[data_base]

    def insert_list(self, collection_name: str, record_list: List[Dict]):
        collection = self.__database[collection_name]
        collection.insert_many(record_list)

    def insert(self, collection_name: str, record: Dict):
        collection = self.__database[collection_name]
        collection.insert(record)

    def __del__(self):
        self.__client.close()
