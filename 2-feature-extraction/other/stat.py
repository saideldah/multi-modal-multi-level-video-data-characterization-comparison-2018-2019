
import xml.dom.minidom

from normalization import utility


def get_max_word_number(file_name):
    input_dom_tree = xml.dom.minidom.parse(file_name)
    words = input_dom_tree.getElementsByTagName("Words")
    max_len = 0
    for word in words:
        length = int(word.getAttribute('length'))
        if length > max_len:
            max_len = length
    # print max_len
    return max_len


def get_max_duration(file_name):
    input_dom_tree = xml.dom.minidom.parse(file_name)
    shots = input_dom_tree.getElementsByTagName("Shot")
    max_duration = 0
    for shot in shots:
        length = float(shot.getAttribute('duration'))
        if length > max_duration:
            max_duration = length
    return max_duration


output_directory_path = "C:/features/structure-analysis-shots-test/"
output_file_name_list = utility.get_file_name_list(output_directory_path)

max_shot_duration = 0
max_shot_word_length = 0
i = 1
l = len(output_file_name_list)
for file_name in output_file_name_list:
    this_shot_duration = get_max_duration(output_directory_path + file_name)
    this_shot_word_length = get_max_word_number(output_directory_path + file_name)
    if this_shot_duration > max_shot_duration:
        max_shot_duration = this_shot_duration

    if this_shot_word_length > max_shot_word_length:
        max_shot_word_length = this_shot_word_length
    utility.print_progress_bar(i, l)
    i = i + 1

print "   "
print "Completed"
print "max_shot_duration: " + str(max_shot_duration)
print "max_shot_word_length: " + str(max_shot_word_length)
