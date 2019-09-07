# coding=utf-8
import codecs
import xml.dom.minidom

import utility


def trim(string_to_trim):
    string_to_trim = string_to_trim.replace('<?xml version="1.0" encoding="utf-8"?>', '').strip()
    return string_to_trim


def xml_fil_to_string(xml_file):
    xml_string = xml_file.open().read()
    xml_string = trim(xml_string)
    return xml_string


def is_valid_xml(xml_file):
    xml_string = xml_fil_to_string(xml_file)
    if utility.is_null_or_whitespaces(xml_string):
        return False
    else:
        return True


def time_to_sec(time_string):
    time_string = time_string.replace("-", "")
    only_time_string = ""
    for i in range(1, 9):
        only_time_string += time_string[i]
    a = only_time_string.split(":")
    seconds = int(a[0]) * 60 * 60 + int(a[1]) * 60 + int(a[2])
    return seconds


def normalize_shot(input_file_path, output_file_path):
    doc = xml.dom.minidom.parse(input_file_path)
    segments = doc.getElementsByTagName("Segment")
    if segments:
        for segment in segments:
            start = segment.getAttribute('start')
            end = segment.getAttribute('end')
            start_sec = time_to_sec(start)
            end_sec = time_to_sec(end)
            segment.setAttribute('end', str(end_sec))
            segment.setAttribute('start', str(start_sec))
            segment.setAttribute('duration', str(end_sec - start_sec))
            print "start: " + str(start_sec)
            print "end: " + str(end_sec)

        key_frames = doc.getElementsByTagName("KeyFrameID")

        for key_frame in key_frames:
            time = key_frame.getAttribute('time')
            time_sec = time_to_sec(time)
            key_frame.setAttribute('time', str(time_sec))
            print "time_sec: " + str(time_sec)

        output_file = codecs.open(output_file_path, 'wb', "utf-8")
        doc.writexml(output_file)
        output_file.close()


# -----------------------------
# application main code

input_directory_path = "D:/Data/test_shots/"
output_directory_path = "D:/Data/test_shots_normalized/"

file_list = utility.get_xml_files(input_directory_path)
for file_to_normalize in file_list:
    print "------------------------------------------------------------------------------------------------------------"

    print file_to_normalize.name
    if is_valid_xml(file_to_normalize):
        normalize_shot(input_directory_path + file_to_normalize.name, output_directory_path + file_to_normalize.name)
    else:
        print "invalid file"
