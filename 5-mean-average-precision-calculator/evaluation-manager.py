import utility as utl
import csv
import collections


class EvaluationManager:
    __clustering_result_set_by_category = {}  # clustering_result_set_by_category[category_label] = [list of clusters]
    __clustering_result_set_by_category_count = 0
    __clustering_result_set_by_cluster = {}  # clustering_result_set_by_cluster[cluster] = [list of categories]
    __clustering_result_set_by_cluster_count = 0
    __cluster_list = []
    __category_list = []
    __input_file_name = ""
    __input_directory_path = ""
    __input_file_path = ""

    def __init__(self, directory_path, file_name):
        self.__input_file_name = file_name
        self.__input_directory_path = directory_path + file_name
        self.__input_file_path = self.__input_directory_path + self.__input_file_name
        self.__fill_clustering_result_set()

    def __fill_clustering_result_set(self):
        with open(self.__input_file_path) as f:
            self.__clustering_result_set_by_category_count = sum(1 for line in f) - 1
        f.close()
        with open(self.__input_file_path, 'r') as csvFile:
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

    def __get_cluster_distribution_per_category(self, cluster_list_per_category):

        clusters_per_category_statistics_dictionary = {}

        for cluster in self.__cluster_list:
            clusters_per_category_statistics_dictionary[str(cluster)] = 0

        for cluster in cluster_list_per_category:
            clusters_per_category_statistics_dictionary[cluster] += 1

        return clusters_per_category_statistics_dictionary

    @staticmethod
    def __convert_to_float(string_vector):
        vector = []
        for item in string_vector:
            vector.append(float(item))
        return vector

    def __calculate_category_distribution_per_cluster(self, category_list_per_cluster):
        categories_per_cluster_statistics_dictionary = {}

        for category in self.__category_list:
            categories_per_cluster_statistics_dictionary[category] = 0

        for category in category_list_per_cluster:
            categories_per_cluster_statistics_dictionary[category] += 1

        return categories_per_cluster_statistics_dictionary

    def generate_cluster_distribution_per_category_csv(self):

        print "creating csv file..."
        output_path = self.__input_directory_path.replace("clustering_results", "evaluation_results")

        with open(
                output_path + "cluster_per_category/" + self.__input_file_name,
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

    def generate_category_distribution_per_cluster_csv(self):

        print "creating csv file..."
        output_path = self.__input_directory_path.replace("clustering_results", "evaluation_results")
        with open(
                output_path + "category_per_cluster/" + self.__input_file_name,
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

    def generate_precision_category_per_cluster_csv(self):
        print "generating precision category per cluster csv..."
        precision_category_per_cluster_input_file = self.__input_directory_path.replace("clustering_results",
                                                                                        "evaluation_results") \
                                                    + "category_per_cluster/" + self.__input_file_name
        iteration = 0
        with open(precision_category_per_cluster_input_file) as csvFile:
            reader = csv.reader(csvFile)
            print("preparing dataset_by_category ...")
            clusters = {}
            categories = []
            for row in reader:
                if iteration > 0:
                    cluster_label = row[0]
                    cluster_distribution_count = EvaluationManager.__convert_to_float()
                    clusters[cluster_label] = cluster_distribution_count
                else:
                    categories = row[1: len(row)]
                iteration += 1
        max_value = iteration - 1
        csvFile.close()
        output_file_path = precision_category_per_cluster_input_file("category_per_cluster",
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

    def generate_precision_cluster_per_category_csv(self):
        print "generate_mean_average_precision_cluster_per_category_csv..."
        precision_category_per_cluster_input_file = self.__input_directory_path.replace("clustering_results",
                                                                                        "evaluation_results") \
                                                    + "cluster_per_category/" + self.__input_file_name
        iteration = 0
        with open(precision_category_per_cluster_input_file) as csvFile:
            reader = csv.reader(csvFile)
            print("preparing dataset_by_category ...")
            categories = {}
            clusters = []
            for row in reader:
                if iteration > 0:
                    category_label = row[0]
                    category_distribution_score = EvaluationManager.__convert_to_float()
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
                "score"
            ]

            the_writer.writerow(headers)
            iteration = 1

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

    def get_accuracy_for_category_per_cluster(self):
        iteration = 0
        with open(self.__input_directory_path + file_name) as csvFile:
            reader = csv.reader(csvFile)
            clusters = {}
            for row in reader:
                if iteration > 0:
                    cluster_label = row[0]
                    category_distribution_count = EvaluationManager.__convert_to_float()
                    clusters[cluster_label] = category_distribution_count
                iteration += 1
        csvFile.close()
        total_max_distribution = 0
        total = 0
        for cluster_label, category_distribution_count in clusters.iteritems():
            total_max_distribution = total_max_distribution + max(category_distribution_count)
            total = total + sum(category_distribution_count)
        return float(total_max_distribution) / float(total)

    def generate_accuracy_for_category_per_cluster_csv(self):
        print "generate_accuracy_for_category_per_cluster_csv..."
        file_name_list = utl.get_file_name_list(self.__input_directory_path)
        accuracy_list = {}
        max_value = len(file_name_list)
        for file_name in file_name_list:
            key = file_name.replace(".csv", "")
            accuracy_list[key] = EvaluationManager.get_accuracy_for_category_per_cluster(self.__input_directory_path,
                                                                                         file_name)

        output_path = self.__input_directory_path.replace("category_per_cluster/", "")
        with open(output_path + "accuracy_for_category_per_cluster.csv", 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "file_name",
                "accuracy",
            ]

            the_writer.writerow(headers)
            iteration = 1

            for file_name, accuracy in accuracy_list.iteritems():
                vector = [file_name, accuracy]
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")

    def __get_accuracy_for_cluster_per_category(self):
        iteration = 0
        with open(self.__input_directory_path + file_name) as csvFile:
            reader = csv.reader(csvFile)
            categories = {}
            for row in reader:
                if iteration > 0:
                    category_label = row[0]
                    cluster_distribution_count = EvaluationManager.__convert_to_float()
                    categories[category_label] = cluster_distribution_count
                iteration += 1
        csvFile.close()
        total_max_distribution = 0
        total = 0
        for category_label, cluster_distribution_count in categories.iteritems():
            total_max_distribution = total_max_distribution + max(cluster_distribution_count)
            total = total + sum(cluster_distribution_count)
        return float(total_max_distribution) / float(total)

    def generate_accuracy_for_cluster_per_category_csv(self):
        print "generate_accuracy_for_category_per_cluster_csv..."
        file_name_list = utl.get_file_name_list(self.__input_directory_path)
        accuracy_list = {}
        max_value = len(file_name_list)
        for file_name in file_name_list:
            key = file_name.replace(".csv", "")
            accuracy_list[key] = EvaluationManager.get_accuracy_for_category_per_cluster(self.__input_directory_path,
                                                                                         file_name)

        output_path = self.__input_directory_path.replace("cluster_per_category/", "")
        with open(output_path + "accuracy_for_cluster_per_category.csv", 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "file_name",
                "accuracy",
            ]

            the_writer.writerow(headers)
            iteration = 1

            for file_name, accuracy in accuracy_list.iteritems():
                vector = [file_name, accuracy]
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")
