import json

import xmltodict
from pathlib import Path


def xml_to_json_string(xml_string: str) -> str:
    dictionary = xmltodict.parse(xml_string)
    json_string = json.dumps(dictionary)
    return json_string


def xml_to_dictionary(xml_string: str) -> dict:
    dictionary: dict = xmltodict.parse(xml_string)
    return dictionary


def get_xml_files(directory: str):
    path = Path(directory)
    return path.glob("*.xml")


def get_file(file_path: str):
    path = Path(file_path)
    return path.open()


def is_null_or_whitespaces(string: str) -> bool:
    if not string.strip():
        return True
    else:
        return False
