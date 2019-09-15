import csv
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import Birch
from sklearn.cluster import MeanShift

import utility


class ClusteringManager:
    __csv_file = ""
    __data_set = []
    __number_of_clusters = 30
    __data_set_count = 0
    __shot_metadata = []

    def __init__(self, csv_file, number_of_clusters):
        self.__data_set = []
        self.__shot_metadata = []
        with open(csv_file) as f:
            self.__data_set_count = sum(1 for line in f) - 1
        f.close()
        self.__csv_file = csv_file
        self.__number_of_clusters = number_of_clusters
        self.__fill_data_set(csv_file)

    @staticmethod
    def __convert_to_float(string_vector):
        vector = []
        for item in string_vector:
            vector.append(float(item))
        return vector

    def __fill_data_set(self, csv_file):
        with open(csv_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            iteration = 0
            print("preparing data...")
            for row in reader:
                if iteration > 0:
                    shot_metadata = [row[0], row[1], row[2], 0]
                    self.__shot_metadata.append(shot_metadata)
                    self.__data_set.append(self.__convert_to_float(row[3:len(row)]))
                    utility.print_progress_bar(iteration, self.__data_set_count)
                iteration += 1
        csvFile.close()
        print("")

    def __generate_result_clustering_csv(self, labels, file_name):
        with open(file_name, 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "video",
                "shot_number",
                "category",
                "cluster"
            ]
            the_writer.writerow(headers)
            for i in range(len(labels)):
                shot_metadata = self.__shot_metadata[i]
                cluster = labels[i]
                vector = [shot_metadata[0], shot_metadata[1], shot_metadata[2], cluster]
                the_writer.writerow(vector)
            f.close()

    def k_means(self, output_file_path):
        print("KMeans Clustering in progress...")
        arr = np.array(self.__data_set)
        kMeans = KMeans(n_clusters=self.__number_of_clusters).fit(arr)
        labels = kMeans.labels_
        print("KMeans Clustering done!")
        print("generating kMeans clustering csv")
        self.__generate_result_clustering_csv(labels, output_file_path)
        print("kMeans clustering csv created successfully!")

    def spectral(self, output_file_path):
        print("Spectral Clustering in progress...")
        arr = np.array(self.__data_set[:10000])
        spectral = SpectralClustering(n_clusters=2).fit(arr)
        labels = spectral.labels_
        self.__generate_result_clustering_csv(labels, output_file_path)
        print("Spectral Clustering done!")

    def db_scan(self, eps, output_file_path):
        # eps: the minimum distance between two points.It means that if
        # the distance between two points is lower or equal
        # to this value(eps), these points are considered neighbors.

        # minPoints: the minimum number of points to form a dense region.For example,
        # if we set the minPoints parameter as 5, then we need at least 5 points to form a dense region.

        print("db_scan Clustering in progress...")
        utility.print_time_now()
        # min_samples = self.__data_set_count / self.__number_of_clusters
        min_samples = 5
        arr = np.array(self.__data_set)
        db_scan = DBSCAN(eps=eps, min_samples=min_samples).fit(arr)
        labels = db_scan.labels_
        print("db_scan Clustering done!")
        utility.print_time_now()
        print("generating db_scan clustering csv")
        self.__generate_result_clustering_csv(labels, output_file_path)
        print("db_scan clustering csv created successfully!")

    def birch(self, output_file_path):
        print("birch Clustering in progress...")
        arr = np.array(self.__data_set)
        birch_clustering = Birch(branching_factor=50, n_clusters=self.__number_of_clusters, threshold=20,
                           compute_labels=False) \
            .fit(arr)
        labels = birch_clustering.labels_
        print("Birch Clustering done!")
        print("generating Birch clustering csv")
        self.__generate_result_clustering_csv(labels, output_file_path)
        print("Birch clustering csv created successfully!")

    def mean_shift(self, output_file_path, bandwidth, n_jobs=4):
        print("mean_shift Clustering in progress...")
        utility.print_time_now()
        arr = np.array(self.__data_set)
        mean_shift_clus = MeanShift(bandwidth=bandwidth, n_jobs=n_jobs).fit(arr)
        labels = mean_shift_clus.labels_
        print("mean_shift Clustering done!")
        print("generating mean_shift clustering csv")
        self.__generate_result_clustering_csv(labels, output_file_path)
        print("mean_shift clustering csv created successfully!")
        utility.print_time_now()


def run_k_means():
    number_of_clusters = 26
    for i in range(10):

        if i == 1:
            number_of_clusters = 30
        else:
            if i > 0:
                number_of_clusters = number_of_clusters + 5

        print("-----------------------------------------------")

        print("number_of_clusters =:" + str(number_of_clusters))

        # Video
        input_video_features = "./input/video_features.csv"
        complete_k_means_output_file = "./clustering_results/kMeans/video/complete-intra-inter/" \
                                      + str(number_of_clusters) + "_kMeans_video_clustering_results.csv"
        input_video_features_cm = ClusteringManager(input_video_features, number_of_clusters=number_of_clusters)
        input_video_features_cm.k_means(complete_k_means_output_file)

        input_normalized_video_features = "./input/normalized_video_features.csv"
        normalized_k_means_output_file = "./clustering_results/kMeans/video/normalized-intra-inter/" \
                                        + str(number_of_clusters) + "_kMeans_video_clustering_results.csv"
        input_video_features_cm = ClusteringManager(input_normalized_video_features,
                                                    number_of_clusters=number_of_clusters)
        input_video_features_cm.k_means(normalized_k_means_output_file)

        # shot

        input_video_features = "./input/shot_features.csv"
        complete_k_means_output_file = "./clustering_results/kMeans/shot/complete-intra-inter/" \
                                             + str(number_of_clusters) + "_kMeans_shot_clustering_results.csv"
        input_video_features_cm = ClusteringManager(input_video_features, number_of_clusters=number_of_clusters)
        input_video_features_cm.k_means(complete_k_means_output_file)

        input_normalized_video_features = "./input/normalized_shot_features.csv"
        normalized_k_means_output_file = "./clustering_results/kMeans/shot/normalized-intra-inter/" \
                                         + str(number_of_clusters) + "_kMeans_shot_clustering_results.csv"
        input_video_features_cm = ClusteringManager(input_normalized_video_features,
                                                    number_of_clusters=number_of_clusters)
        input_video_features_cm.k_means(normalized_k_means_output_file)

        # complete_video_features

        input_video_features = "./input/complete_video_features.csv"
        complete_k_means_output_file = "./clustering_results/kMeans/complete_video/complete-intra-inter/" \
                                       + str(number_of_clusters) + "_k_means.csv"
        input_video_features_cm = ClusteringManager(input_video_features, number_of_clusters=number_of_clusters)
        input_video_features_cm.k_means(complete_k_means_output_file)

        input_normalized_video_features = "./input/normalized_complete_video_features.csv"
        normalized_k_means_output_file = "./clustering_results/kMeans/complete_video/normalized-intra-inter/" \
                                         + str(number_of_clusters) + "_k_means.csv"
        input_video_features_cm = ClusteringManager(input_normalized_video_features,
                                                    number_of_clusters=number_of_clusters)
        input_video_features_cm.k_means(normalized_k_means_output_file)


def run_db_scan():
    number_of_clusters = 26
    for i in range(1):

        if i == 1:
            number_of_clusters = 30
        else:
            if i > 0:
                number_of_clusters = number_of_clusters + 5

        print("-----------------------------------------------")

        print("number_of_clusters =:" + str(number_of_clusters))
        # input_video_features = "./input/video_features.csv"

        # Video
        # video_db_scan_output_file = "./clustering_results/db_scan/video/complete-intra-inter/" \
        #                             + str(number_of_clusters) + "_db_scan.csv"
        # input_video_features_cm = ClusteringManager(input_video_features, number_of_clusters=number_of_clusters)
        # input_video_features_cm.db_scan(50, video_db_scan_output_file)

        input_normalized_video_features = "./input/normalized_video_features.csv"
        normalized_db_scan_output_file = "./clustering_results/db_scan/video/normalized-intra-inter/" \
                                         + str(number_of_clusters) + "_db_scan.csv"
        input_video_features_cm = ClusteringManager(input_normalized_video_features,
                                                    number_of_clusters=number_of_clusters)
        input_video_features_cm.db_scan(15, normalized_db_scan_output_file)

        # shot

        # input_shot_features = "./input/shot_features.csv"
        # complete_db_scan_output_file = "./clustering_results/db_scan/shot/complete-intra-inter/" \
        #                                + str(number_of_clusters) + "_db_scan.csv"
        # input_video_features_cm = ClusteringManager(input_shot_features, number_of_clusters=number_of_clusters)
        # input_video_features_cm.db_scan(complete_db_scan_output_file)
        #
        # input_normalized_shot_features = "./input/normalized_shot_features.csv"
        # normalized_db_scan_output_file = "./clustering_results/db_scan/shot/normalized-intra-inter/" \
        #                                  + str(number_of_clusters) + "_db_scan.csv"
        # input_video_features_cm = ClusteringManager(input_normalized_shot_features,
        #                                             number_of_clusters=number_of_clusters)
        # input_video_features_cm.db_scan(output_file_path=normalized_db_scan_output_file)

        # complete_video_features

        # input_video_features = "./input/complete_video_features.csv"
        # complete_k_means_output_file = "./clustering_results/db_scan/complete_video/complete-intra-inter/" \
        #                                + str(number_of_clusters) + "_db_scan.csv"
        # input_video_features_cm = ClusteringManager(input_video_features, number_of_clusters=number_of_clusters)
        # input_video_features_cm.db_scan(complete_k_means_output_file)
        #
        # input_normalized_video_features = "./input/normalized_complete_video_features.csv"
        # normalized_k_means_output_file = "./clustering_results/db_scan/complete_video/normalized-intra-inter/" \
        #                                  + str(number_of_clusters) + "_db_scan.csv"
        # input_video_features_cm = ClusteringManager(input_normalized_video_features,
        #                                             number_of_clusters=number_of_clusters)
        # input_video_features_cm.db_scan(normalized_k_means_output_file)


def main():
    run_db_scan()


main()
