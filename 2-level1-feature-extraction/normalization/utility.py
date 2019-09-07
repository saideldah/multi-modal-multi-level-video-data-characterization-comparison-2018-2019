import json
import os
import xml
import sys
import xmltodict
from pathlib import Path


def xml_to_json_string(xml_string):
    dictionary = xmltodict.parse(xml_string)
    json_string = json.dumps(dictionary)
    return json_string


def xml_to_dictionary(xml_string):
    dictionary = xmltodict.parse(xml_string)
    return dictionary


def get_xml_files(directory):
    path = Path(directory)
    return path.glob("*.xml")


def get_file(file_path):
    path = Path(file_path)
    return path.open()


def is_null_or_whitespaces(string):
    if not string.strip():
        return True
    else:
        return False


def get_file_name_list(directory_path):
    file_list = os.listdir(directory_path)
    return file_list


def is_valid_shot(seg_start, seg_end, shot_start, shot_end):
    if shot_start <= seg_start < shot_end and shot_start < seg_end <= shot_end:
        return True
    else:
        return False


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def get_shots(input_file):
    doc = xml.dom.minidom.parse(input_file)
    segments = doc.getElementsByTagName("Segment")
    shots = []
    if segments:
        for segment in segments:
            start = float(segment.getAttribute('start'))
            end = float(segment.getAttribute('end'))
            duration = float(segment.getAttribute('duration'))
            entry = {"start": start, "end": end, "duration": duration}
            if duration > 2:
                shots.append(entry)
    return shots


def remove_file(path):
    os.remove(path)


def print_progress_bar(iteration, max_val):
    percentage = (iteration * 100) / max_val
    bar = "["
    for i in range(percentage):
        bar = bar + "#"

    for i in range(percentage, 100):
        bar = bar + "-"
    bar = bar + "]"
    sys.stdout.write("\r" + bar + "%d%%" % percentage + "[" + str(iteration) +
                     "/" + str(max_val) + "]")
    sys.stdout.flush()
