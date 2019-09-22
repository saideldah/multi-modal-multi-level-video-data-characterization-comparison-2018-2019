import utility as utl
import operator

import csv


class Video:
    name = ""
    category = ""
    shots = {}

    def __init__(self):
        self.name = ""
        self.category = ""
        self.shots = {}
        pass


def get_videos_dictionary(input_file_path):
    videos_dictionary = {}
    with open(input_file_path) as f:
        data_set_count = sum(1 for line in f) - 1
    f.close()
    algorithms_names = ["kNN", "Logistic_Regression", "Neural_Network", "SVM", "Random_Forest", "Naive_Bayes",
                        "AdaBoost"]
    with open(input_file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        iteration = 0
        print("preparing dataset_by_category ...")

        for row in reader:
            if iteration > 0:
                category = row[0]
                video_name = row[1]
                shot_number = row[2]
                algorithms_results = row[3:len(row)]
                if video_name not in videos_dictionary:
                    videos_dictionary[video_name] = Video()
                    videos_dictionary[video_name].category = category
                    videos_dictionary[video_name].name = video_name
                    videos_dictionary[video_name].shots = {}
                if shot_number not in videos_dictionary[video_name].shots:
                    videos_dictionary[video_name].shots[shot_number] = {}
                i = 0
                for algorithms_name in algorithms_names:
                    videos_dictionary[video_name].shots[shot_number][algorithms_name] = algorithms_results[i]
                    i += 1
                utl.print_progress_bar(iteration + 1, data_set_count)
            iteration += 1
    csvFile.close()
    return videos_dictionary, algorithms_names


def get_max_repeated_category(list_of_categories):
    categories_counter = {}
    for category in list_of_categories:
        if category not in categories_counter:
            categories_counter[category] = 0
        categories_counter[category] += 1
    # print categories_counter
    # print ""
    return max(categories_counter.iteritems(), key=operator.itemgetter(1))[0]


def get_dominant_category_vector(video):
    vector = [video.name, video.category]
    categories_per_algorithm = {}
    for shot, algorithms_results in video.shots.iteritems():
        for algorithm_name, algorithm_category in algorithms_results.iteritems():
            if algorithm_name not in categories_per_algorithm:
                categories_per_algorithm[algorithm_name] = []
            categories_per_algorithm[algorithm_name].append(algorithm_category)
    for algorithm_name, list_of_categories in categories_per_algorithm.iteritems():
        max_cat = get_max_repeated_category(list_of_categories)
        vector.append(max_cat)

    return vector


def generate_dominant_category_csv(input_file_path, output_file_path):
    videos_dictionary, algorithms_names = get_videos_dictionary(input_file_path)

    print ""
    print "generating generate category feature csv"
    with open(output_file_path, 'wb') as f:
        the_writer = csv.writer(f)
        headers = ["video", "category"] + algorithms_names
        the_writer.writerow(headers)
        iteration = 1
        max_value = len(videos_dictionary)
        for video_name, video_object in videos_dictionary.iteritems():
            vector = get_dominant_category_vector(video_object)
            the_writer.writerow(vector)
            utl.print_progress_bar(iteration, max_value)
            iteration += 1
        f.close()


def generate_classification_accuracy(input_file, output_file):
    well_classified_counter_dic = {}
    with open(input_file) as f:
        total_videos_count = sum(1 for line in f) - 1
    f.close()

    algorithms_names = ["kNN", "Logistic_Regression", "Neural_Network", "SVM", "Random_Forest", "Naive_Bayes",
                        "AdaBoost"]
    for algorithm_name in algorithms_names:
        well_classified_counter_dic[algorithm_name] = 0

    with open(input_file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        iteration = 0
        print ""
        print("preparing dataset_by_category ...")

        for row in reader:
            if iteration > 0:
                category = row[1]
                algorithms_results = row[2:len(row)]
                i = 0
                for algorithm_name in algorithms_names:
                    if category == algorithms_results[i]:
                        well_classified_counter_dic[algorithm_name] += 1
                    i += 1
                utl.print_progress_bar(iteration + 1, total_videos_count)
            iteration += 1
    csvFile.close()
    algorithm_score = {}
    for algorithm_name, well_classified_counter in well_classified_counter_dic.iteritems():
        algorithm_score[algorithm_name] = float(well_classified_counter) / float(total_videos_count)

    print ""
    print "generating generate category feature csv"
    with open(output_file, 'wb') as f:
        the_writer = csv.writer(f)
        the_writer.writerow(algorithms_names)
        iteration = 1
        max_value = len(algorithm_score)
        vector = []
        for algorithm_name, accuracy in algorithm_score.iteritems():
            vector.append(accuracy)
            utl.print_progress_bar(iteration, max_value)
            iteration += 1
        the_writer.writerow(vector)
        f.close()


def main():
    # input_file = "./classification_results/Dev_Features_Shots_Normalized_CV10_withoutDefault_Output_final.tsv"
    # output_file = "./classification_results/Dev_Features_Shots_Normalized_CV10_withoutDefault_Output_final.csv"
    #
    # utl.tsc_to_csv(input_file, output_file)

    # input_file = "./classification_results/Dev_Features_Shots_Normalized_CV10_Output_final.csv"
    # output_file = "./classification_results/Dev_Features_Shots_CV10_Output_dominant_category.csv"

    # input_file = "./classification_results/Dev_Features_Shots_Normalized_CV10_withoutDefault_Output_final.csv"
    # output_file = "./classification_results/Dev_Features_Shots_CV10_withoutDefault_Output_dominant_category.csv"
    #
    # generate_dominant_category_csv(input_file, output_file)

    input_file = "./classification_results/Dev_Features_Shots_CV10_Output_dominant_category.csv"
    output_file = "./classification_results/Dev_Features_Shots_CV10_Output_dominant_category_accuracy.csv"
    input_file1 = "./classification_results/Dev_Features_Shots_CV10_withoutDefault_Output_dominant_category.csv"
    output_file1 = "./classification_results/Dev_Features_Shots_CV10_withoutDefault_Output_dominant_category_accuracy.csv"
    generate_classification_accuracy(input_file, output_file)
    generate_classification_accuracy(input_file1, output_file1)


main()
