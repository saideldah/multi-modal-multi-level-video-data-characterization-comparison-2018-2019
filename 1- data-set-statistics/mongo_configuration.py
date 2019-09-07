import json
from pathlib import Path
from typing import Dict


class MongoConfiguration:
    __config: Dict[str, str] = {}
    __database: str
    __server: str
    __port: str

    def __init__(self):
        path = Path("mongo_configuration.json")
        json_string = path.open().read()
        self.__config = json.loads(json_string)
        self.__server = self.__config["server"]
        self.__port = self.__config["port"]
        self.__database = self.__config["database"]

    @property
    def database(self):
        return self.__database

    @property
    def server(self):
        return self.__server

    @property
    def port(self):
        return self.__port
