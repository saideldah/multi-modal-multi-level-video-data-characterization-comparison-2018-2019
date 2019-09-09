import utility as utl
import csv


class MeanAveragePrecisionCalculator:
    def __init__(self, directory_path, file_name):
        self.__file_name = file_name
        self.__file_path = directory_path + file_name

    @staticmethod
    def __fill_data_set_by_category(csv_file):
        with open(csv_file) as f:
            data_set_count = sum(1 for line in f) - 1
        f.close()
        with open(csv_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            iteration = 0
            print("preparing dataset_by_category ...")
            dataset_by_category = {}
            clusters = []
            for row in reader:
                if iteration > 0:
                    category = row[2]
                    cluster = row[3]
                    if category not in dataset_by_category:
                        dataset_by_category[category] = []
                    if int(cluster) not in clusters:
                        clusters.append(int(cluster))

                    dataset_by_category[category].append(cluster)
                    utl.print_progress_bar(iteration + 1, data_set_count)
                iteration += 1
        csvFile.close()
        print("")
        return dataset_by_category, clusters

    @staticmethod
    def __fill_data_set_by_cluster(csv_file):
        with open(csv_file) as f:
            data_set_count = sum(1 for line in f) - 1
        f.close()
        with open(csv_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            iteration = 0
            print("preparing dataset_by_category ...")
            dataset_by_cluster = {}
            categories = []
            for row in reader:
                if iteration > 0:
                    category = row[2]
                    cluster = row[3]
                    cluster_label = "cluster" + cluster
                    if cluster_label not in dataset_by_cluster:
                        dataset_by_cluster[cluster_label] = []
                    if category not in categories:
                        categories.append(category)

                    dataset_by_cluster[cluster_label].append(category)
                    utl.print_progress_bar(iteration + 1, data_set_count)
                iteration += 1
        csvFile.close()
        print("")
        return dataset_by_cluster, categories

    @staticmethod
    def __calculate_cluster_distribution_per_category(list_of_clusters, list_of_category_clusters):
        list_of_clusters.sort()

        clusters_dictionary = {}

        for cluster in list_of_clusters:
            clusters_dictionary[str(cluster)] = 0

        for cluster in list_of_category_clusters:
            clusters_dictionary[cluster] += 1

        return clusters_dictionary

    @staticmethod
    def __calculate_category_distribution_per_cluster(categories, categories_per_cluster):
        categories.sort()
        category_dic = {}

        for category in categories:
            category_dic[category] = 0

        for category in categories_per_cluster:
            category_dic[category] += 1

        return category_dic

    @staticmethod
    def generate_cluster_distribution_per_category_csv(directory_path, file_name):
        dataset_by_category, clusters = MeanAveragePrecisionCalculator.__fill_data_set_by_category(
            directory_path + file_name)
        print "creating csv file..."
        output_path = directory_path.replace("clustering_results", "mean-average-precision")

        with open(
                output_path + "cluster-per-category/" + file_name,
                'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "category"
            ]
            clusters.sort()
            for cluster in clusters:
                headers.append("cluster " + str(cluster))
                # print str(cluster)
            the_writer.writerow(headers)
            iteration = 1
            max_value = len(dataset_by_category)

            for key, value in dataset_by_category.iteritems():
                vector = [key]
                cluster_stat_dic = MeanAveragePrecisionCalculator.__calculate_cluster_distribution_per_category(
                    clusters, value)
                for key1, value1 in cluster_stat_dic.iteritems():
                    vector.append(value1)
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")

    @staticmethod
    def generate_category_distribution_per_cluster_csv(directory_path, file_name):
        dataset_by_cluster, categories = MeanAveragePrecisionCalculator.__fill_data_set_by_cluster(
            directory_path + file_name)

        print "creating csv file..."
        output_path = directory_path.replace("clustering_results", "mean-average-precision")
        with open(
                output_path + "category-per-cluster/" + file_name,
                'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "cluster"
            ]
            categories.sort()
            for category in categories:
                headers.append(category)
            the_writer.writerow(headers)
            iteration = 1
            max_value = len(dataset_by_cluster)

            for key, value in dataset_by_cluster.iteritems():
                cluster = key
                vector = [cluster]
                categories_per_cluster = value
                cluster_stat_dic = MeanAveragePrecisionCalculator.__calculate_category_distribution_per_cluster(
                    categories, categories_per_cluster)
                for key1, value1 in cluster_stat_dic.iteritems():
                    vector.append(value1)
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")

    @staticmethod
    def __convert_to_float(string_vector):
        vector = []
        for item in string_vector:
            vector.append(float(item))
        return vector

    @staticmethod
    def generate_mean_average_precision_category_per_cluster_csv(directory_path,
                                                                 file_name):
        print "generating mean average precision category per cluster csv..."
        iteration = 0
        with open(directory_path + file_name) as csvFile:
            reader = csv.reader(csvFile)
            print("preparing dataset_by_category ...")
            clusters = {}
            categories = []
            for row in reader:
                if iteration > 0:
                    cluster_label = row[0]
                    cluster_distribution_score = MeanAveragePrecisionCalculator.__convert_to_float(row[1: len(row)])
                    clusters[cluster_label] = cluster_distribution_score
                else:
                    categories = row[1: len(row)]
                iteration += 1
        max_value = iteration - 1
        csvFile.close()
        output_path = directory_path.replace("category-per-cluster", "")
        with open(output_path + "map-category-per-cluster/" + file_name, 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "cluster",
                "category",
                "score"
            ]

            the_writer.writerow(headers)
            iteration = 1

            for cluster_label, cluster_distribution_score in clusters.iteritems():
                max_feature = max(cluster_distribution_score)
                total = sum(cluster_distribution_score)
                index_of_max_feature = cluster_distribution_score.index(max_feature)
                score = max_feature / total
                vector = [cluster_label, categories[index_of_max_feature], score]
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")

    @staticmethod
    def generate_mean_average_precision_cluster_per_category_csv(directory_path,
                                                                 file_name):
        print "generating mean average precision category per cluster csv..."
        iteration = 0
        with open(directory_path + file_name) as csvFile:
            reader = csv.reader(csvFile)
            print("preparing dataset_by_category ...")
            categories = {}
            clusters = []
            for row in reader:
                if iteration > 0:
                    category_label = row[0]
                    category_distribution_score = MeanAveragePrecisionCalculator.__convert_to_float(row[1: len(row)])
                    categories[category_label] = category_distribution_score
                else:
                    clusters = row[1: len(row)]
                iteration += 1
        max_value = iteration - 1
        csvFile.close()
        output_path = directory_path.replace("cluster-per-category", "")
        with open(output_path + "map-cluster-per-category/" + file_name, 'wb') as f:
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


def generate_distribution_csv_files(directory_path):
    clustering_results_file_name_list = utl.get_file_name_list(directory_path)
    for file_name in clustering_results_file_name_list:
        if file_name != "merged-with-features" \
                and file_name != "cluster-distribution-per-category" \
                and file_name != "category-distribution-per-cluster":
            print ("generating " + file_name)
            MeanAveragePrecisionCalculator.generate_cluster_distribution_per_category_csv(
                directory_path,
                file_name)
            MeanAveragePrecisionCalculator.generate_category_distribution_per_cluster_csv(
                directory_path,
                file_name)
            print ("---------------------------------------------------------------")


def generate_mean_average_precision_category_per_cluster_csv_files(directory_path):
    file_name_list = utl.get_file_name_list(directory_path)
    for file_name in file_name_list:
        print ("generating mean_average_precision for " + file_name)
        MeanAveragePrecisionCalculator.generate_mean_average_precision_category_per_cluster_csv(directory_path,
                                                                                                file_name)
        print ("---------------------------------------------------------------")


def generate_mean_average_precision_cluster_per_category_csv_files(directory_path):
    file_name_list = utl.get_file_name_list(directory_path)
    for file_name in file_name_list:
        print ("generating mean_average_precision for " + file_name)
        MeanAveragePrecisionCalculator.generate_mean_average_precision_cluster_per_category_csv(directory_path,
                                                                                                file_name)
        print ("---------------------------------------------------------------")


def main():
    # directory_path_list = [
    #     "./clustering_results/kMeans/shot/complete-intra-inter/"
    #     , "./clustering_results/kMeans/shot/normalized-intra-inter/"
    #     , "./clustering_results/kMeans/video/complete-intra-inter/"
    #     , "./clustering_results/kMeans/video/normalized-intra-inter/"
    # ]
    # for directory_path in directory_path_list:
    #     generate_distribution_csv_files(directory_path)

    # generate_mean_average_precision_category_per_cluster_csv_files
    # map_directory_path_list = [
    #     "./mean-average-precision/kMeans/shot/complete-intra-inter/category-per-cluster/"
    #     , "./mean-average-precision/kMeans/shot/normalized-intra-inter/category-per-cluster/"
    #     , "./mean-average-precision/kMeans/video/complete-intra-inter/category-per-cluster/"
    #     , "./mean-average-precision/kMeans/video/normalized-intra-inter/category-per-cluster/"
    # ]
    # for map_directory_path in map_directory_path_list:
    #     generate_mean_average_precision_category_per_cluster_csv_files(map_directory_path)

    # generate_mean_average_precision_cluster_per_category_csv_files
    map_directory_path_list = [
        "./mean-average-precision/kMeans/shot/complete-intra-inter/cluster-per-category/"
        , "./mean-average-precision/kMeans/shot/normalized-intra-inter/cluster-per-category/"
        , "./mean-average-precision/kMeans/video/complete-intra-inter/cluster-per-category/"
        , "./mean-average-precision/kMeans/video/normalized-intra-inter/cluster-per-category/"
    ]
    for map_directory_path in map_directory_path_list:
        generate_mean_average_precision_cluster_per_category_csv_files(map_directory_path)


main()
