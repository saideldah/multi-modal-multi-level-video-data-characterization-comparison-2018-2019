import utility as utl
import csv
import threading
import numpy as np


def convert_to_float(string_vector):
    vector = []
    for item in string_vector:
        vector.append(float(item))
    return vector


def fill_data_set(csv_file):
    with open(csv_file) as f:
        data_set_count = sum(1 for line in f) - 1
    f.close()
    with open(csv_file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        iteration = 0
        print("preparing dataset_by_category ...")
        dataset_by_category = {}
        for row in reader:
            if iteration > 0:
                category = row[2]
                if category not in dataset_by_category:
                    dataset_by_category[category] = []

                dataset_by_category[category].append(convert_to_float(row[3:len(row)]))
                utl.print_progress_bar(iteration, data_set_count)
            iteration += 1
    csvFile.close()
    print("")
    return dataset_by_category


def calculate_mean(vector):
    total = sum(vector)
    return total / len(vector)


def calculate_distance_mean(category, category_data_set):
    print("calculating distance mean for '" + category + "' category  ...")

    category_data_set_len = len(category_data_set)  # type: int
    distance_list = []
    for i in range(0, category_data_set_len):
        for j in range(i + 1, category_data_set_len):
            vec1 = category_data_set[i]
            vec2 = category_data_set[j]
            distance_list.append(utl.calculate_distance(vec1, vec2))
        utl.print_progress_bar(i + 1, category_data_set_len)
    print("")
    print("distance mean calculation for category '" + category + "' has been completed!")

    return calculate_mean(distance_list)


def generate_category_mean_csv():
    dataset_by_category_result = fill_data_set("shot_features.csv")

    category_mean_list = {}
    for key, value in dataset_by_category_result.iteritems():
        mean = calculate_distance_mean(key, value)
        category_mean_list[key] = mean

    for key, value in category_mean_list.iteritems():
        print key, str(value)

    print "creating csv file..."
    with open('category_mean.csv', 'wb') as f:
        the_writer = csv.writer(f)
        headers = [
            "category",
            "distance_mean"
        ]
        the_writer.writerow(headers)
        iteration = 1
        max_value = len(category_mean_list)

        for key, value in category_mean_list.iteritems():
            vector = [key, value]
            the_writer.writerow(vector)
            utl.print_progress_bar(iteration, max_value)
            iteration += 1
        f.close()
        print("")
        print("csv file has been created successfully")


distance_arr = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]


def calculate_distance(vec1, vec2, result_index):
    a = np.array(vec1)
    b = np.array(vec2)

    distance_arr[result_index] = np.linalg.norm(a - b)


def clean_distance_arr():
    for i in range(len(distance_arr)):
        distance_arr[i] = 0


def remove_zeros(arr):
    res = []
    for item in arr:
        if item > 0:
            res.append(item)
    return res


def calculate_two_categories_distance_mean(category_set1, category_set2):
    category_set1_len = len(category_set1)
    category_set2_len = len(category_set2)
    max_value = category_set1_len * category_set2_len
    iteration = 1
    distance_list = []
    category_set2_length = len(category_set2)
    for vector1 in category_set1:
        for i in range(category_set2_length):
            i1 = i + 1
            i2 = i + 2
            i3 = i + 3
            i4 = i + 4
            i5 = i + 4
            i6 = i + 4
            i7 = i + 4
            i8 = i + 1
            i9 = i + 2
            i10 = i + 3
            i11 = i + 4
            i12 = i + 4
            i13 = i + 4
            i14 = i + 4

            v = category_set2[i]
            t = threading.Thread(target=calculate_distance, args=(vector1, v, 0,))
            t1 = threading.Thread()
            t2 = threading.Thread()
            t3 = threading.Thread()
            t4 = threading.Thread()
            t5 = threading.Thread()
            t6 = threading.Thread()
            t7 = threading.Thread()
            t8 = threading.Thread()
            t9 = threading.Thread()
            t10 = threading.Thread()
            t11 = threading.Thread()
            t12 = threading.Thread()
            t13 = threading.Thread()
            t14 = threading.Thread()

            t.start()
            if i1 < category_set2_length:
                v1 = category_set2[i1]
                t1 = threading.Thread(target=calculate_distance, args=(vector1, v1, 1,))
                t1.start()
            if i2 < category_set2_length:
                v2 = category_set2[i2]
                t2 = threading.Thread(target=calculate_distance, args=(vector1, v2, 2,))
                t2.start()
            if i3 < category_set2_length:
                v3 = category_set2[i3]
                t3 = threading.Thread(target=calculate_distance, args=(vector1, v3, 3,))
                t3.start()
            if i4 < category_set2_length:
                v4 = category_set2[i4]
                t4 = threading.Thread(target=calculate_distance, args=(vector1, v4, 4,))
                t4.start()
            if i5 < category_set2_length:
                v5 = category_set2[i2]
                t5 = threading.Thread(target=calculate_distance, args=(vector1, v5, 5,))
                t5.start()
            if i6 < category_set2_length:
                v6 = category_set2[i3]
                t6 = threading.Thread(target=calculate_distance, args=(vector1, v6, 6,))
                t6.start()
            if i7 < category_set2_length:
                v7 = category_set2[i4]
                t7 = threading.Thread(target=calculate_distance, args=(vector1, v7, 7,))
                t7.start()
            if i8 < category_set2_length:
                v8 = category_set2[i8]
                t8 = threading.Thread(target=calculate_distance, args=(vector1, v8, 8,))
                t8.start()
            if i9 < category_set2_length:
                v9 = category_set2[i9]
                t9 = threading.Thread(target=calculate_distance, args=(vector1, v9, 9,))
                t9.start()
            if i10 < category_set2_length:
                v10 = category_set2[i10]
                t10 = threading.Thread(target=calculate_distance, args=(vector1, v10, 10,))
                t10.start()
            if i11 < category_set2_length:
                v11 = category_set2[i11]
                t11 = threading.Thread(target=calculate_distance, args=(vector1, v11, 11,))
                t11.start()
            if i12 < category_set2_length:
                v12 = category_set2[i12]
                t12 = threading.Thread(target=calculate_distance, args=(vector1, v12, 12,))
                t12.start()
            if i13 < category_set2_length:
                v13 = category_set2[i13]
                t13 = threading.Thread(target=calculate_distance, args=(vector1, v13, 13,))
                t13.start()
            if i14 < category_set2_length:
                v14 = category_set2[i14]
                t14 = threading.Thread(target=calculate_distance, args=(vector1, v14, 14,))
                t14.start()

            t.join()

            if i1 < category_set2_length:
                t1.join()
            if i2 < category_set2_length:
                t2.join()
            if i3 < category_set2_length:
                t3.join()
            if i4 < category_set2_length:
                t4.join()
            if i5 < category_set2_length:
                t5.join()
            if i6 < category_set2_length:
                t6.join()
            if i7 < category_set2_length:
                t7.join()
            if i8 < category_set2_length:
                t8.join()
            if i9 < category_set2_length:
                t9.join()
            if i10 < category_set2_length:
                t10.join()
            if i11 < category_set2_length:
                t11.join()
            if i12 < category_set2_length:
                t12.join()
            if i13 < category_set2_length:
                t13.join()
            if i14 < category_set2_length:
                t14.join()
            distance_list = distance_list + remove_zeros(distance_arr)
            utl.print_progress_bar(iteration, max_value)
            clean_distance_arr()
            iteration += 15
    print ""
    return sum(distance_list) / len(distance_list)


def create_csv_file(two_category_distance_mean_list):
    print "creating different category mean csv file..."
    with open('different_category_mean.csv', 'wb') as f:
        the_writer = csv.writer(f)
        headers = [
            "category1",
            "category2",
            "distance_mean"
        ]
        the_writer.writerow(headers)
        iteration = 1
        max_value = len(two_category_distance_mean_list)
        for vector in two_category_distance_mean_list:
            the_writer.writerow(vector)
            utl.print_progress_bar(iteration, max_value)
            iteration += 1

        print("")
        print("csv file has been created successfully")


def generate_different_category_mean_csv():
    dataset_by_category_result = fill_data_set("shot_features.csv")

    key_list = []
    for key, value in dataset_by_category_result.iteritems():
        key_list.append(key)

    two_category_distance_mean_list = []
    for i in range(len(key_list)):
        for j in range(i + 1, len(key_list)):
            category_set1 = dataset_by_category_result[key_list[i]]
            category_set2 = dataset_by_category_result[key_list[j]]
            print "calculating distance mean between " + key_list[i] + " and " + key_list[j]
            two_category_distance_mean = calculate_two_categories_distance_mean(category_set1, category_set2)
            two_category_distance_mean_list.append([key_list[i], key_list[j], two_category_distance_mean])
            print "calculating distance mean between " + key_list[i] + " and " + key_list[j] + " has been done!"
            create_csv_file(two_category_distance_mean_list)


def main():
    generate_different_category_mean_csv()


main()
