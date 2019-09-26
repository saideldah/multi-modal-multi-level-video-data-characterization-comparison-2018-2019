import utility as utl
import csv


def calculate_vectors_average(vectors):
    result = [0] * len(vectors[0])
    total_vectors = len(vectors)
    for vector in vectors:
        result = map(sum, zip(vector, result))
    for i in range(0, len(result)):
        result[i] = result[i] / total_vectors
    return result


def convert_to_float(string_vector):
    vector = []
    for item in string_vector:
        vector.append(float(item))
    return vector


def get_category_features_dictionary_from_complete_features(input_file_path):
    category_features = {}
    with open(input_file_path) as f:
        data_set_count = sum(1 for line in f) - 1
    f.close()
    with open(input_file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        iteration = 0
        print("preparing dataset_by_category ...")

        for row in reader:
            if iteration > 0:
                category = row[2]
                feature_vector = convert_to_float(row[3: len(row)])
                if category not in category_features:
                    category_features[category] = []
                category_features[category].append(feature_vector)

                utl.print_progress_bar(iteration + 1, data_set_count)
            iteration += 1
    csvFile.close()
    return category_features


def generate_category_feature(input_file_path, output_file_path):
    category_features = get_category_features_dictionary_from_complete_features(input_file_path)

    category_average_features = {}

    for category, category_feature_vector_list in category_features.iteritems():
        category_average_features[category] = calculate_vectors_average(category_feature_vector_list)
    print "generating generate category feature csv"
    with open(output_file_path, 'wb') as f:
        the_writer = csv.writer(f)
        headers = [
            "video"
            "category",
            "interactions_number_speakers_2",
            "interactions_number_speakers_3",
            "interactions_number_speakers_4",
            "interactions_number_speakers_4+",
            "intervention_short",
            "intervention_long",
            "speakers_type_ponctuel",
            "speakers_type_localise",
            "speakers_type_present",
            "speakers_type_regulier",
            "speakers_type_important",
            "speaker_distribution",
            "mean_number_of_faces",
            "std_number_of_faces",
            "inter_intensity_variation",
            "intra_intensity_variation",
            "number_shot_transition",
            "number_speaker_transition",
            "speech",
            "music",
            "speech_with_music",
            "speech_with_non_music",
            "non_speech_with_music",
            "non_speech_with_non_music",
            "words",
            "duration"
        ]
        the_writer.writerow(headers)
        iteration = 1
        max_value = len(category_average_features)
        for category, category_feature_vector in category_average_features.iteritems():
            vector = [category] + category_feature_vector
            the_writer.writerow(vector)
            utl.print_progress_bar(iteration, max_value)
            iteration += 1
        f.close()


def get_category_features_dictionary(input_file_path):
    category_features = {}
    with open(input_file_path) as f:
        data_set_count = sum(1 for line in f) - 1
    f.close()
    with open(input_file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        iteration = 0
        print("preparing dataset_by_category ...")

        for row in reader:
            if iteration > 0:
                category = row[0]
                feature_vector = convert_to_float(row[1: len(row)])
                if category not in category_features:
                    category_features[category] = []
                category_features[category].append(feature_vector)

                utl.print_progress_bar(iteration + 1, data_set_count)
            iteration += 1
    csvFile.close()
    return category_features


def generate_category_feature_distribution(features_file_path, input_file_path, output_file_path):
    category_features = get_category_features_dictionary(input_file_path)
    category_self_distance_dictionary = get_category_self_distance_dictionary(features_file_path, input_file_path)
    category_distance_dictionary = {}
    categories = []
    for category, category_feature_vector in category_features.iteritems():
        categories.append(category)
        for category2, category_feature_vector2 in category_features.iteritems():
            if category != category2:
                dist = utl.calculate_distance(category_feature_vector, category_feature_vector2)
            else:
                dist = category_self_distance_dictionary[category]

            category_distance_dictionary[category + "_" + category2] = dist

    print "generating generate category feature csv"
    with open(output_file_path, 'wb') as f:
        the_writer = csv.writer(f)
        headers = ["category"] + categories
        the_writer.writerow(headers)
        iteration = 1
        max_value = len(category_distance_dictionary)
        for category in categories:
            vector = [category]
            for category2 in categories:
                vector.append(category_distance_dictionary[category + "_" + category2])
            the_writer.writerow(vector)
            utl.print_progress_bar(iteration, max_value)
            iteration += 1
        f.close()


def mean(numbers):
    return float(sum(numbers)) / float(len(numbers))


def get_category_self_distance_dictionary(features_file_path, category_average_file_path):
    category_complete_features = get_category_features_dictionary_from_complete_features(
        features_file_path)
    category_average_features = get_category_features_dictionary(category_average_file_path)
    category_distance_dictionary = {}
    for category_name_average, category_average_feature_vector in category_average_features.iteritems():
        category_distance_dictionary[category_name_average] = []
        for category_complete_feature_vector in category_complete_features[category_name_average]:
            distance = utl.calculate_distance(category_average_feature_vector, category_complete_feature_vector)
            category_distance_dictionary[category_name_average].append(distance)
    category_average_distance_dictionary = {}
    for category, distance_list in category_distance_dictionary.iteritems():
        category_average_distance_dictionary[category] = mean(distance_list)

    return category_average_distance_dictionary


def main():
    input_output_list = [
        ["./features/normalized_shot_features.csv", "category_average_shot_features.csv"],
        ["./features/normalized_video_features.csv", "category_average_video_features.csv"],
        ["./features/normalized_complete_video_features.csv", "category_average_complete_video_features.csv"]
    ]
    for input_output in input_output_list:
        print "generating " + input_output[1]
        generate_category_feature(input_output[0], input_output[1])

    input_output_list2 = [
        ["./features/normalized_shot_features.csv", "category_average_shot_features.csv",
         "category_shot_distance_distribution_with_self_distance.csv"],
        ["./features/normalized_video_features.csv", "category_average_video_features.csv",
         "category_video_distance_distribution_with_self_distance.csv"],
        ["./features/normalized_complete_video_features.csv", "category_average_complete_video_features.csv",
         "category_complete_video_distance_distribution_with_self_distance.csv"]
    ]
    for input_output in input_output_list2:
        print "generating " + input_output[1]
        generate_category_feature_distribution(input_output[0], input_output[1], input_output[2])

    # input_output_list3 = [
    #     ["./features/normalized_shot_features.csv", "category_average_shot_features.csv",
    #      "category_shot_self_distance.csv"],
    #     ["./features/normalized_video_features.csv", "category_average_video_features.csv",
    #      "category_video_self_distance.csv"],
    #     ["./features/normalized_complete_video_features.csv", "category_average_complete_video_features.csv",
    #      "category_complete_video_self_distance.csv"]
    # ]
    # for input_output in input_output_list3:
    #     print "generating " + input_output[1]
    #     generate_category_self_distance_csv(input_output[0], input_output[1], input_output[2])
    #     break


main()
