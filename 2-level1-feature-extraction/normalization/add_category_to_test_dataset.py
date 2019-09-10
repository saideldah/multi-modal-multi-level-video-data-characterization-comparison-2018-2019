import csv
import xml

import utility
import codecs
import xml.dom.minidom
from xml.dom.minidom import Document


def convert_to_csv(txt_file_path, headers):
    print ""
    print "generating " + txt_file_path + " csv file"
    f = open(txt_file_path, "r")
    csv_rows = [headers]
    output = txt_file_path.replace(".txt", ".csv")
    for line in f:
        csv_rows.append(line.split())
    f.close()
    with open(output, 'wb') as csv_f:
        the_writer = csv.writer(csv_f)
        iteration = 1
        max_value = len(csv_rows)
        for row in csv_rows:
            the_writer.writerow(row)
            utility.print_progress_bar(iteration, max_value)
            iteration += 1
        csv_f.close()


def get_category_codes_dictionary(category_codes_csv_file_path):
    with open(category_codes_csv_file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        iteration = 0
        print("preparing clustering results data ...")
        category_codes_dictionary = {}
        for row in reader:
            if iteration > 0:
                category_codes_dictionary[row[0]] = row[1]
            iteration += 1
    csvFile.close()
    print("")
    return category_codes_dictionary


def get_video_with_category_code_dictionary(video_with_category_csv_file_path):
    with open(video_with_category_csv_file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        iteration = 0
        print("preparing clustering results data ...")
        video_with_category_code_dictionary = {}
        for row in reader:
            if iteration > 0:
                video_with_category_code_dictionary[row[2]] = row[0]
            iteration += 1
    csvFile.close()
    print("")
    return video_with_category_code_dictionary


def generate_category_video_name_csv(category_codes_csv_file_path, video_with_category_csv_file_path):
    category_codes_dictionary = get_category_codes_dictionary(category_codes_csv_file_path)
    video_with_category_code_dictionary = get_video_with_category_code_dictionary(video_with_category_csv_file_path)
    with open("category_with_video.csv", 'wb') as csv_f:
        the_writer = csv.writer(csv_f)
        iteration = 1
        max_value = len(video_with_category_code_dictionary)
        the_writer.writerow(["video_name", "category"])
        for video_name, category_code in video_with_category_code_dictionary.iteritems():
            the_writer.writerow([video_name, category_codes_dictionary[category_code]])
            utility.print_progress_bar(iteration, max_value)
            iteration += 1
        csv_f.close()


def get_video_with_category_dictionary(video_with_category_csv_file_path):
    with open(video_with_category_csv_file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        iteration = 0
        print("preparing clustering results data ...")
        video_with_category_dictionary = {}
        for row in reader:
            if iteration > 0:
                video_with_category_dictionary[row[0]] = row[1]
            iteration += 1
    csvFile.close()
    print("")
    return video_with_category_dictionary


def add_category_to_xml(input_path, output_path, full_file_name, video_with_category_dictionary):
    input_dom_tree = xml.dom.minidom.parse(input_path)
    video_name = full_file_name.replace(".xml", "")
    metadata_element = input_dom_tree.getElementsByTagName("Metadata")
    category_element = input_dom_tree.createElement("Category")
    category = video_with_category_dictionary[video_name]
    category_element.appendChild(input_dom_tree.createTextNode(category))
    metadata_element[0].appendChild(category_element)

    file_handle = codecs.open(output_path, 'wb', 'utf8')
    input_dom_tree.writexml(file_handle)
    file_handle.close()


def add_category_to_test_data():
    video_with_category_dictionary = get_video_with_category_dictionary("category_with_video.csv")
    test_directory_path = "C:/code/features/input/structure_analysis/test/"
    for i in range(1, 5):
        directory = test_directory_path + str(i) + "/"
        file_name_list = utility.get_file_name_list(directory)
        iteration = 1
        max_value = len(file_name_list)
        print ""
        print "normalizing " + directory
        for file_name in file_name_list:
            input_path = directory + file_name
            output_path = test_directory_path + "normalized/" + str(i) + "/" + file_name
            add_category_to_xml(input_path, output_path, file_name, video_with_category_dictionary)
            utility.print_progress_bar(iteration, max_value)
            iteration += 1


def main():
    add_category_to_test_data()
    # category_codes_file_path = "CategoryCodes.txt"
    # category_codes_headers = ["code", "category"]
    # video_with_category_file_path = "Video_With_Category.txt"
    # video_with_category_headers = ["code", "number", "video_name", "number"]
    #
    # convert_to_csv(category_codes_file_path, category_codes_headers)
    # convert_to_csv(video_with_category_file_path, video_with_category_headers)
    #
    # generate_category_video_name_csv("CategoryCodes.csv", "Video_With_Category.csv")


main()
