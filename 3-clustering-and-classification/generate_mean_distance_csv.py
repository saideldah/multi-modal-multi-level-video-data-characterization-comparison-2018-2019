import csv

import utility


def convert_to_float(string_vector):
    vector = []
    for item in string_vector:
        vector.append(float(item))
    return vector


def get_features_list(csv_file):
    data_set = []
    with open(csv_file) as f:
        data_set_count = sum(1 for line in f) - 1
    with open(csv_file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        iteration = 0
        print("")

        print("preparing data...")
        for row in reader:
            if iteration > 0:
                shot_metadata = [row[0], row[1], row[2], 0]
                shot_metadata.append(shot_metadata)
                data_set.append(convert_to_float(row[3:len(row)]))
                utility.print_progress_bar(iteration, data_set_count)
            else:
                data_set_count -= 1
            iteration += 1
    csvFile.close()
    print("")
    return data_set


def generate_average_distance_csv(features_csv, distance_output):
    feature_vectors = get_features_list(features_csv)
    feature_vector_count = len(feature_vectors)

    print "generating distance csv..."
    distance_count = 0
    distance_sum = 0
    iteration = 1
    for i in range(feature_vector_count):
        if i + 1 > feature_vector_count:
            break
        for j in range(i + 1, feature_vector_count):
            v1 = feature_vectors[i]
            v2 = feature_vectors[j]
            distance_sum += utility.calculate_distance(v1, v2)
            distance_count += 1
        utility.print_progress_bar(iteration, feature_vector_count)
        iteration += 1

    with open(distance_output, 'wb') as f:
        the_writer = csv.writer(f)
        headers = [
            "file",
            "average_distance"
        ]
        the_writer.writerow(headers)
        vector = [features_csv, float(distance_sum) / float(distance_count)]
        the_writer.writerow(vector)
        f.close()


def main():
    files = [
        "./input/complete_video_features.csv",
        "./input/normalized_complete_video_features.csv",
        "./input/video_features.csv",
        "./input/normalized_video_features.csv",
    ]
    for f in files:
        output = f.replace(".csv", "") + "_distance.csv"
        generate_average_distance_csv(f, output)


main()
