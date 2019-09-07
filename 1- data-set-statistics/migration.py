import utility
from mongo_configuration import MongoConfiguration
from mongo_repository import MongoRepository


class MigrationManager:
    def __init__(self):
        mongo_config = MongoConfiguration()
        self.__mongo_repository: MongoRepository = MongoRepository(mongo_config.server, mongo_config.port,
                                                                   mongo_config.database)

    @staticmethod
    def __trim(string_to_trim: str) -> str:
        string_to_trim = string_to_trim.replace('ï»؟', '') \
            .replace('<?xml version="1.0" encoding="utf-8"?>', '').strip()
        return string_to_trim

    def __xml_fil_to_string(self, xml_file) -> str:
        xml_string = xml_file.open().read()
        xml_string = self.__trim(xml_string)
        return xml_string

    def migrate_to_mongo(self, directory: str, mongo_collection: str):
        dev_xml_files = utility.get_xml_files(directory)
        count = 0
        for xml in dev_xml_files:
            xml_string = self.__xml_fil_to_string(xml)
            if not utility.is_null_or_whitespaces(xml_string):
                count += 1
                print(count)
                print(xml)
                dictionary = utility.xml_to_dictionary(xml_string)
                self.__mongo_repository.insert(mongo_collection, dictionary)

    @staticmethod
    def __time_to_sec(time_string: str) -> int:
        time_string = time_string.replace("-", "")
        only_time_string = ""
        for i in range(1, 9):
            only_time_string += time_string[i]
        a = only_time_string.split(":")
        seconds = int(a[0]) * 60 * 60 + int(a[1]) * 60 + int(a[2])
        return seconds

    def migrate_shots_to_mongo(self, directory: str, mongo_collection: str):
        dev_xml_files = utility.get_xml_files(directory)
        count = 0
        for xml in dev_xml_files:
            xml_string = self.__xml_fil_to_string(xml)
            if not utility.is_null_or_whitespaces(xml_string):
                count += 1
                print(count)
                print(xml)
                dictionary = utility.xml_to_dictionary(xml_string)
                if "Segmentation" in dictionary and "Segments" in dictionary["Segmentation"] and "Segment" in \
                        dictionary["Segmentation"]["Segments"]:
                    segments = dictionary["Segmentation"]["Segments"]["Segment"]
                    if isinstance(segments, list):
                        for segment in segments:
                            segment["@start"] = self.__time_to_sec(segment["@start"])
                            segment["@end"] = self.__time_to_sec(segment["@end"])
                            segment["duration"] = segment["@end"] - segment["@start"]
                    else:
                        segments["@start"] = self.__time_to_sec(segments["@start"])
                        segments["@end"] = self.__time_to_sec(segments["@end"])
                        segments["duration"] = segments["@end"] - segments["@start"]

                self.__mongo_repository.insert(mongo_collection, dictionary)
