import utility as utl
import csv


class CategoryClusterDistributionCalculator:
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
        dataset_by_category, clusters = CategoryClusterDistributionCalculator.__fill_data_set_by_category(
            directory_path + file_name)
        print "creating csv file..."
        with open(directory_path + 'cluster_distribution_per_category.csv', 'wb') as f:
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
                cluster_stat_dic = CategoryClusterDistributionCalculator.__calculate_cluster_distribution_per_category(
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
        dataset_by_cluster, categories = CategoryClusterDistributionCalculator.__fill_data_set_by_cluster(
            directory_path + file_name)
        print "creating csv file..."
        with open(directory_path + 'category_distribution_per_cluster.csv', 'wb') as f:
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
                cluster_stat_dic = CategoryClusterDistributionCalculator.__calculate_category_distribution_per_cluster(
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
    def generate_dominant_category_distribution_per_cluster_csv(directory_path):
        output_file_path = directory_path + "generate_dominant_category_distribution_per_cluster.csv"
        input_dile_path = directory_path + 'category_distribution_per_cluster.csv'
        print "generate_dominant_category_distribution_pe_cluster_csv..."
        iteration = 0
        with open(input_dile_path) as csvFile:
            reader = csv.reader(csvFile)
            print("preparing dataset_by_category ...")
            clusters = {}
            categories = []
            for row in reader:
                if iteration > 0:
                    cluster_label = row[0]
                    cluster_features = CategoryClusterDistributionCalculator.__convert_to_float(row[1: len(row)])
                    clusters[cluster_label] = cluster_features
                else:
                    categories = row[1: len(row)]
                iteration += 1
        max_value = iteration
        csvFile.close()

        with open(output_file_path, 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "cluster",
                "category",
                "score"
            ]

            the_writer.writerow(headers)
            iteration = 1

            for cluster_label, cluster_features in clusters.iteritems():
                max_feature = max(cluster_features)
                total = sum(cluster_features)
                index_of_max_feature = cluster_features.index(max_feature)
                score = max_feature / total
                vector = [cluster_label, categories[index_of_max_feature], score]
                the_writer.writerow(vector)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()
            print("")
            print("csv file has been created successfully")


def main():
    # directory_path = "clustering_results/k_means/"
    # file_name = "k_means_clustering_results.csv"
    directory_path = "clustering_results/k_means/"
    file_name = "k_means_clustering_results.csv"
    CategoryClusterDistributionCalculator.generate_cluster_distribution_per_category_csv(directory_path, file_name)
    CategoryClusterDistributionCalculator.generate_category_distribution_per_cluster_csv(directory_path, file_name)
    CategoryClusterDistributionCalculator.generate_dominant_category_distribution_per_cluster_csv(directory_path)


main()
