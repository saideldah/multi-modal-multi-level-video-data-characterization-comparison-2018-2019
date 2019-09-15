import utility as utl
import csv
import collections
import os


class EvaluationManager:
    __clustering_result_set_by_category = {}  # clustering_result_set_by_category[category_label] = [list of clusters]
    __clustering_result_set_by_category_count = 0
    __clustering_result_set_by_cluster = {}  # clustering_result_set_by_cluster[cluster] = [list of categories]
    __clustering_result_set_by_cluster_count = 0
    __cluster_list = []
    __category_list = []
    # __input_file_name = ""
    __input_directory_path = ""

    # __input_file_path = ""

    def __init__(self, directory_path):
        # self.__input_file_name = file_name
        self.__input_directory_path = directory_path
        # self.__input_file_path = self.__input_directory_path + self.__input_file_name

    # region private
    def __fill_clustering_result_set(self, file_name):
        with open(self.__input_directory_path + file_name) as f:
            self.__clustering_result_set_by_category_count = sum(1 for line in f) - 1
        f.close()
        with open(self.__input_directory_path + file_name, 'r') as csvFile:
            reader = csv.reader(csvFile)
            iteration = 0
            print("preparing dataset_by_category ...")
            dataset_by_category = {}
            clusters = []
            dataset_by_cluster = {}
            categories = []

            for row in reader:
                if iteration > 0:
                    category = row[2]
                    cluster = row[3]

                    if category not in dataset_by_category:
                        dataset_by_category[category] = []
                    if int(cluster) not in clusters:
                        clusters.append(int(cluster))

                    dataset_by_category[category].append(cluster)

                    if cluster not in dataset_by_cluster:
                        dataset_by_cluster[cluster] = []
                    if category not in categories:
                        categories.append(category)

                    dataset_by_cluster[cluster].append(category)

                    utl.print_progress_bar(iteration + 1, self.__clustering_result_set_by_category_count)
                iteration += 1
        csvFile.close()
        print("")
        self.__clustering_result_set_by_category = dataset_by_category
        self.__cluster_list = clusters
        self.__category_list = categories
        self.__clustering_result_set_by_cluster = dataset_by_cluster
        self.__cluster_list.sort()
        self.__category_list.sort()
        self.__clustering_result_set_by_category = collections.OrderedDict(
            sorted(self.__clustering_result_set_by_category.items()))
        self.__clustering_result_set_by_cluster = collections.OrderedDict(
            sorted(self.__clustering_result_set_by_cluster.items()))
        self.__clustering_result_set_by_category_count = len(self.__clustering_result_set_by_category)
        self.__clustering_result_set_by_cluster_count = len(self.__clustering_result_set_by_cluster)

    def __generate_cluster_distribution_per_category_csv(self, file_name):

        print "creating csv file..."
        output_path = self.__input_directory_path.replace("clustering_results", "evaluation_results")

        with open(
                output_path + "cluster_per_category/" + file_name,
                'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "category"
            ]

            for cluster in self.__cluster_list:
                headers.append("cluster " + str(cluster))
                # print str(cluster)
            the_writer.writerow(headers)
            iteration = 1

            for category, cluster_list_per_category in self.__clustering_result_set_by_category.iteritems():
                vector = [category]
                clusters_per_category_statistics_dictionary = self.__get_cluster_distribution_per_category(
                    cluster_list_per_category)
                for category2, stat in clusters_per_category_statistics_dictionary.iteritems():
                    vector.append(stat)
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, self.__clustering_result_set_by_category_count)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")

    def __generate_category_distribution_per_cluster_csv(self, file_name):

        print "creating csv file..."
        output_path = self.__input_directory_path.replace("clustering_results", "evaluation_results")
        with open(
                output_path + "category_per_cluster/" + file_name,
                'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "cluster"
            ]
            for category in self.__category_list:
                headers.append(category)
            the_writer.writerow(headers)
            iteration = 1

            for cluster, category_list_per_cluster in self.__clustering_result_set_by_cluster.iteritems():
                vector = [cluster]
                categories_per_cluster_statistics_dictionary = self.__calculate_category_distribution_per_cluster(
                    category_list_per_cluster)
                for cluster2, stat in categories_per_cluster_statistics_dictionary.iteritems():
                    vector.append(stat)
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, self.__clustering_result_set_by_cluster_count)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")

    def __get_cluster_distribution_per_category(self, cluster_list_per_category):

        clusters_per_category_statistics_dictionary = {}

        for cluster in self.__cluster_list:
            clusters_per_category_statistics_dictionary[str(cluster)] = 0

        for cluster in cluster_list_per_category:
            clusters_per_category_statistics_dictionary[cluster] += 1

        return clusters_per_category_statistics_dictionary

    def __calculate_category_distribution_per_cluster(self, category_list_per_cluster):
        categories_per_cluster_statistics_dictionary = {}

        for category in self.__category_list:
            categories_per_cluster_statistics_dictionary[category] = 0

        for category in category_list_per_cluster:
            categories_per_cluster_statistics_dictionary[category] += 1

        return categories_per_cluster_statistics_dictionary

    def __generate_precision_category_per_cluster_csv(self, file_name):
        print "generating precision category per cluster csv..."
        precision_category_per_cluster_input_file = self.__input_directory_path.replace("clustering_results",
                                                                                        "evaluation_results") \
                                                    + "category_per_cluster/" + file_name
        iteration = 0
        with open(precision_category_per_cluster_input_file) as csvFile:
            reader = csv.reader(csvFile)
            print("preparing dataset_by_category ...")
            clusters = {}
            categories = []
            for row in reader:
                if iteration > 0:
                    cluster_label = row[0]
                    cluster_distribution_count = EvaluationManager.__convert_to_float(row[1:len(row)])
                    clusters[cluster_label] = cluster_distribution_count
                else:
                    categories = row[1: len(row)]
                iteration += 1
        max_value = iteration - 1
        csvFile.close()
        output_file_path = precision_category_per_cluster_input_file.replace("category_per_cluster",
                                                                             "precision_category_per_cluster")
        with open(output_file_path, 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "cluster",
                "category",
                "precision"
            ]

            the_writer.writerow(headers)
            iteration = 1
            clusters = collections.OrderedDict(
                sorted(clusters.items()))

            for cluster_label, cluster_distribution_count in clusters.iteritems():
                max_feature = max(cluster_distribution_count)
                total = sum(cluster_distribution_count)
                index_of_max_feature = cluster_distribution_count.index(max_feature)
                score = max_feature / total
                vector = [cluster_label, categories[index_of_max_feature], score]
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")

    def __generate_precision_cluster_per_category_csv(self, file_name):
        print "generate_mean_average_precision_cluster_per_category_csv..."
        precision_category_per_cluster_input_file = self.__input_directory_path.replace("clustering_results",
                                                                                        "evaluation_results") \
                                                    + "cluster_per_category/" + file_name
        iteration = 0
        with open(precision_category_per_cluster_input_file) as csvFile:
            reader = csv.reader(csvFile)
            print("preparing dataset_by_category ...")
            categories = {}
            clusters = []
            for row in reader:
                if iteration > 0:
                    category_label = row[0]
                    category_distribution_score = EvaluationManager.__convert_to_float(row[1:len(row)])
                    categories[category_label] = category_distribution_score
                else:
                    clusters = row[1: len(row)]
                iteration += 1
        max_value = iteration - 1
        csvFile.close()
        output_file_path = precision_category_per_cluster_input_file.replace("cluster_per_category",
                                                                             "precision_cluster_per_category")
        with open(output_file_path, 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "category",
                "cluster",
                "precision"
            ]

            the_writer.writerow(headers)
            iteration = 1
            categories = collections.OrderedDict(
                sorted(categories.items()))

            for category_label, category_distribution_score in categories.iteritems():
                max_feature = max(category_distribution_score)
                total = sum(category_distribution_score)
                index_of_max_feature = category_distribution_score.index(max_feature)
                score = max_feature / total
                vector = [category_label, clusters[index_of_max_feature], score]
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")

    @staticmethod
    def __get_accuracy_for_category_per_cluster(category_per_cluster_csv):
        iteration = 0
        with open(category_per_cluster_csv) as csvFile:
            reader = csv.reader(csvFile)
            clusters = {}
            for row in reader:
                if iteration > 0:
                    cluster_label = row[0]
                    category_distribution_count = EvaluationManager.__convert_to_float(row[1:len(row)])
                    clusters[cluster_label] = category_distribution_count
                iteration += 1
        csvFile.close()
        total_max_distribution = 0
        total = 0
        for cluster_label, category_distribution_count in clusters.iteritems():
            total_max_distribution = total_max_distribution + max(category_distribution_count)
            total = total + sum(category_distribution_count)
        return float(total_max_distribution) / float(total)

    @staticmethod
    def __get_mean_average_precision(category_per_cluster_csv):
        iteration = 0
        precision_sum = 0
        count = 0
        with open(category_per_cluster_csv) as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if iteration > 0:
                    precision_sum += float(row[2])
                    count += 1
                iteration += 1
        csvFile.close()
        return float(precision_sum) / float(count)

    @staticmethod
    def __get_accuracy_for_cluster_per_category(cluster_per_category_csv):
        iteration = 0
        with open(cluster_per_category_csv) as csvFile:
            reader = csv.reader(csvFile)
            categories = {}
            for row in reader:
                if iteration > 0:
                    category_label = row[0]
                    cluster_distribution_count = EvaluationManager.__convert_to_float(row[1:len(row)])
                    categories[category_label] = cluster_distribution_count
                iteration += 1
        csvFile.close()
        total_max_distribution = 0
        total = 0
        for category_label, cluster_distribution_count in categories.iteritems():
            total_max_distribution = total_max_distribution + max(cluster_distribution_count)
            total = total + sum(cluster_distribution_count)
        return float(total_max_distribution) / float(total)

    @staticmethod
    def __convert_to_float(string_vector):
        vector = []
        for item in string_vector:
            vector.append(float(item))
        return vector

    def __generate_accuracy_for_category_per_cluster_csv(self):
        print "generate_accuracy_for_category_per_cluster_csv..."
        category_per_cluster_directory = self.__input_directory_path.replace("clustering_results",
                                                                             "evaluation_results") \
                                         + "category_per_cluster/"
        file_name_list = utl.get_file_name_list(category_per_cluster_directory)
        accuracy_list = {}
        max_value = len(file_name_list)
        for file_name in file_name_list:
            key = file_name.replace(".csv", "")
            category_per_cluster_csv = category_per_cluster_directory + file_name
            accuracy_list[key] = EvaluationManager.__get_accuracy_for_category_per_cluster(category_per_cluster_csv)

        output_path = category_per_cluster_directory.replace("category_per_cluster/", "")
        with open(output_path + "accuracy_for_category_per_cluster.csv", 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "file_name",
                "accuracy",
            ]

            the_writer.writerow(headers)
            iteration = 1
            accuracy_list = collections.OrderedDict(
                sorted(accuracy_list.items()))
            for file_name, accuracy in accuracy_list.iteritems():
                vector = [file_name, accuracy]
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")

    def __generate_accuracy_for_cluster_per_category_csv(self):
        print "generate_accuracy_for_category_per_cluster_csv..."
        cluster_per_category_directory = self.__input_directory_path.replace("clustering_results",
                                                                             "evaluation_results") \
                                         + "cluster_per_category/"
        file_name_list = utl.get_file_name_list(cluster_per_category_directory)
        accuracy_list = {}
        max_value = len(file_name_list)
        for file_name in file_name_list:
            key = file_name.replace(".csv", "")
            cluster_per_category_csv = cluster_per_category_directory + file_name
            accuracy_list[key] = EvaluationManager.__get_accuracy_for_cluster_per_category(cluster_per_category_csv)

        output_path = cluster_per_category_directory.replace("cluster_per_category/", "")
        with open(output_path + "accuracy_for_cluster_per_category.csv", 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "file_name",
                "accuracy",
            ]

            the_writer.writerow(headers)
            iteration = 1
            accuracy_list = collections.OrderedDict(
                sorted(accuracy_list.items()))
            for file_name, accuracy in accuracy_list.iteritems():
                vector = [file_name, accuracy]
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")

    def __generate_mean_average_precision_cluster_per_category_csv(self):
        print "generate_mean_average_precision_cluster_per_category_csv..."
        precision_cluster_per_category_directory = self.__input_directory_path.replace("clustering_results",
                                                                                       "evaluation_results") \
                                                   + "precision_cluster_per_category/"
        file_name_list = utl.get_file_name_list(precision_cluster_per_category_directory)
        accuracy_list = {}
        max_value = len(file_name_list)
        for file_name in file_name_list:
            key = file_name.replace(".csv", "")
            category_per_cluster_csv = precision_cluster_per_category_directory + file_name
            accuracy_list[key] = EvaluationManager.__get_mean_average_precision(category_per_cluster_csv)

        output_path = precision_cluster_per_category_directory.replace("precision_cluster_per_category/", "")
        with open(output_path + "mean_average_precision_cluster_per_category.csv", 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "file_name",
                "map",
            ]

            the_writer.writerow(headers)
            iteration = 1
            accuracy_list = collections.OrderedDict(
                sorted(accuracy_list.items()))
            for file_name, accuracy in accuracy_list.iteritems():
                vector = [file_name, accuracy]
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")

    def __generate_mean_average_precision_category_per_cluster_csv(self):
        print "generate_mean_average_precision_category_per_cluster_csv..."
        precision_category_per_cluster_directory = self.__input_directory_path.replace("clustering_results",
                                                                                       "evaluation_results") \
                                                   + "precision_category_per_cluster/"
        file_name_list = utl.get_file_name_list(precision_category_per_cluster_directory)
        accuracy_list = {}
        max_value = len(file_name_list)
        for file_name in file_name_list:
            key = file_name.replace(".csv", "")
            category_per_cluster_csv = precision_category_per_cluster_directory + file_name
            accuracy_list[key] = EvaluationManager.__get_mean_average_precision(category_per_cluster_csv)

        output_path = precision_category_per_cluster_directory.replace("precision_category_per_cluster/", "")
        with open(output_path + "mean_average_precision_category_per_cluster.csv", 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "file_name",
                "map",
            ]

            the_writer.writerow(headers)
            iteration = 1
            accuracy_list = collections.OrderedDict(
                sorted(accuracy_list.items()))
            for file_name, accuracy in accuracy_list.iteritems():
                file_name = file_name.replace("k_means", "").replace("birch", "").replace("mean_shift", "").replace(
                    "db_scan", "")
                vector = [file_name, accuracy]
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")

    # endregion

    # region public

    def generate_distribution_files(self, file_name):
        self.__fill_clustering_result_set(file_name)
        self.__generate_cluster_distribution_per_category_csv(file_name)
        self.__generate_category_distribution_per_cluster_csv(file_name)

    def generate_precision_files(self, file_name):
        self.__generate_precision_category_per_cluster_csv(file_name)
        self.__generate_precision_cluster_per_category_csv(file_name)

    def generate_mean_average_precision_files(self):
        self.__generate_mean_average_precision_category_per_cluster_csv()
        self.__generate_mean_average_precision_cluster_per_category_csv()

    def generate_accuracy_files(self):
        self.__generate_accuracy_for_cluster_per_category_csv()
        self.__generate_accuracy_for_category_per_cluster_csv()
    # endregion


def clear(directory):
    print directory
    for parent, dirnames, filenames in os.walk(directory):
        for fn in filenames:
            if fn.lower().endswith('.csv'):
                os.remove(os.path.join(parent, fn))


def main():
    # print "generate_distribution_csv_files"
    directory_path_list = [
        "./clustering_results/k_means/complete_video/",
        "./clustering_results/k_means/video/",
        "./clustering_results/k_means/shot/",
        "./clustering_results/birch/complete_video/",
        "./clustering_results/birch/video/",
        "./clustering_results/db_scan/complete_video/",
        "./clustering_results/db_scan/video/",
        "./clustering_results/mean_shift/complete_video/",
        "./clustering_results/mean_shift/video/"
    ]
    clear("./evaluation_results")

    for directory_path in directory_path_list:
        evaluation_manager = EvaluationManager(directory_path)

        clustering_results_file_name_list = utl.get_file_name_list(directory_path)
        for file_name in clustering_results_file_name_list:
            if file_name != "merged-with-features" \
                    and file_name != "cluster-per-category" \
                    and file_name != "category-per-cluster":
                print ("generating " + file_name)
                evaluation_manager.generate_distribution_files(file_name)
                evaluation_manager.generate_precision_files(file_name)
                print ("---------------------------------------------------------------")
        evaluation_manager.generate_mean_average_precision_files()
        evaluation_manager.generate_accuracy_files()
    print "--------------------------------------------------------------"
    # generate_mean_average_precision_category_per_cluster_csv_files


main()
