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
    __data_set_count = 0
    __shot_metadata = []

    def __init__(self, csv_file):
        self.__data_set = []
        self.__shot_metadata = []
        with open(csv_file) as f:
            self.__data_set_count = sum(1 for line in f) - 1
        f.close()
        self.__csv_file = csv_file
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

    def k_means(self, number_of_clusters, output_file_path):
        print("KMeans Clustering in progress...")
        arr = np.array(self.__data_set)
        k_means = KMeans(n_clusters=number_of_clusters).fit(arr)
        labels = k_means.labels_
        print("KMeans Clustering done!")
        print("generating k_means clustering csv")
        self.__generate_result_clustering_csv(labels, output_file_path)
        print("k_means clustering csv created successfully!")

    def spectral(self, number_of_clusters, output_file_path):
        print("Spectral Clustering in progress...")
        arr = np.array(self.__data_set[:10000])
        spectral = SpectralClustering(n_clusters=number_of_clusters).fit(arr)
        labels = spectral.labels_
        self.__generate_result_clustering_csv(labels, output_file_path)
        print("Spectral Clustering done!")

    def db_scan(self, eps, min_samples, output_file_path):
        # eps: the minimum distance between two points.It means that if
        # the distance between two points is lower or equal
        # to this value(eps), these points are considered neighbors.

        # minPoints: the minimum number of points to form a dense region.For example,
        # if we set the minPoints parameter as 5, then we need at least 5 points to form a dense region.

        print("db_scan Clustering in progress...")
        utility.print_time_now()
        # min_samples = self.__data_set_count / self.__number_of_clusters
        arr = np.array(self.__data_set)
        db_scan = DBSCAN(eps=eps, min_samples=min_samples).fit(arr)
        labels = db_scan.labels_
        print("db_scan Clustering done!")
        utility.print_time_now()
        print("generating db_scan clustering csv")
        self.__generate_result_clustering_csv(labels, output_file_path)
        print("db_scan clustering csv created successfully!")

    def birch(self, number_of_clusters, output_file_path):
        print("birch Clustering in progress...")
        arr = np.array(self.__data_set)
        birch_clustering = Birch(branching_factor=50, n_clusters=number_of_clusters, threshold=20,
                                 compute_labels=False).fit(arr)
        labels = birch_clustering.predict(arr)
        print("Birch Clustering done!")
        print("generating Birch clustering csv")
        self.__generate_result_clustering_csv(labels, output_file_path)
        print("Birch clustering csv created successfully!")

    def mean_shift(self, bandwidth, output_file_path):
        print("mean_shift Clustering in progress...")
        utility.print_time_now()
        arr = np.array(self.__data_set)
        n_jobs = 4
        mean_shift_cluster = MeanShift(bandwidth=bandwidth, n_jobs=n_jobs).fit(arr)
        labels = mean_shift_cluster.labels_
        print("mean_shift Clustering done!")
        print("generating mean_shift clustering csv")
        self.__generate_result_clustering_csv(labels, output_file_path)
        print("mean_shift clustering csv created successfully!")
        utility.print_time_now()


def run_k_means():
    print "Video"
    input_normalized_video_features = "./input/normalized_video_features.csv"
    input_video_features_cm = ClusteringManager(input_normalized_video_features)

    print "Shots"
    input_normalized_video_features = "./input/normalized_shot_features.csv"
    input_shot_features_cm = ClusteringManager(input_normalized_video_features)

    print "Complete Videos"
    input_normalized_video_features = "./input/normalized_complete_video_features.csv"
    input_complete_video_features_cm = ClusteringManager(input_normalized_video_features)

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

        normalized_k_means_output_file = "./clustering_results/k_means/video/" \
                                         + str(number_of_clusters) + "_k_means.csv"

        input_video_features_cm.k_means(number_of_clusters, normalized_k_means_output_file)

        # complete_video

        normalized_k_means_output_file = "./clustering_results/k_means/complete_video/" \
                                         + str(number_of_clusters) + "_k_means.csv"
        input_shot_features_cm.k_means(number_of_clusters, normalized_k_means_output_file)

        # complete_video_features

        normalized_k_means_output_file = "./clustering_results/k_means/complete_video/" \
                                         + str(number_of_clusters) + "_k_means.csv"
        input_complete_video_features_cm.k_means(number_of_clusters, normalized_k_means_output_file)


def run_birch():
    print "Video"
    input_normalized_video_features = "./input/normalized_video_features.csv"
    input_video_features_cm = ClusteringManager(input_normalized_video_features)

    # print "Shots"
    # input_normalized_video_features = "./input/normalized_shot_features.csv"
    # input_shot_features_cm = ClusteringManager(input_normalized_video_features)

    print "Complete Videos"
    input_normalized_video_features = "./input/normalized_complete_video_features.csv"
    input_complete_video_features_cm = ClusteringManager(input_normalized_video_features)

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

        normalized_birch_output_file = "./clustering_results/birch/video/" \
                                       + str(number_of_clusters) + "_birch.csv"

        input_video_features_cm.birch(number_of_clusters, normalized_birch_output_file)

        # complete_video

        # normalized_birch_output_file = "./clustering_results/birch/complete_video/" \
        #                                  + str(number_of_clusters) + "_birch.csv"
        # input_shot_features_cm.birch(number_of_clusters, normalized_birch_output_file)

        # complete_video_features

        normalized_birch_output_file = "./clustering_results/birch/complete_video/" \
                                       + str(number_of_clusters) + "_birch.csv"
        input_complete_video_features_cm.birch(number_of_clusters, normalized_birch_output_file)


def run_db_scan():
    input_normalized_video_features = "./input/normalized_video_features.csv"

    input_video_features_cm = ClusteringManager(input_normalized_video_features)

    eps = 5
    for i in range(10):
        print("-----------------------------------------------")

        print("eps =" + str(eps))

        # Video
        normalized_db_scan_output_file = "./clustering_results/db_scan/video/" \
                                         + str(eps) + "_db_scan.csv"
        input_video_features_cm.db_scan(eps, 5, normalized_db_scan_output_file)
        eps += 5

    input_normalized_video_features = "./input/normalized_complete_video_features.csv"
    input_video_features_cm = ClusteringManager(input_normalized_video_features)
    eps = 25
    for i in range(10):
        # complete_video_features
        print("-----------------------------------------------")

        print("eps =" + str(eps))
        normalized_db_scan_output_file = "./clustering_results/db_scan/complete_video/" \
                                         + str(eps) + "_db_scan.csv"
        input_video_features_cm.db_scan(eps, 5, normalized_db_scan_output_file)
        eps += 5


def run_mean_shift():
    print "complete_video_features"
    input_normalized_video_features = "./input/normalized_video_features.csv"

    input_video_features_cm = ClusteringManager(input_normalized_video_features)

    bandwidth = 55
    for i in range(10):
        print("-----------------------------------------------")

        print("bandwidth =" + str(bandwidth))

        # Video
        normalized_mean_shift_output_file = "./clustering_results/mean_shift/video/" \
                                            + str(bandwidth) + "_mean_shift.csv"
        input_video_features_cm.mean_shift(bandwidth, normalized_mean_shift_output_file)
        bandwidth += 5

    print "complete_video_features"
    input_normalized_video_features = "./input/normalized_complete_video_features.csv"
    input_video_features_cm = ClusteringManager(input_normalized_video_features)
    bandwidth = 75
    for i in range(10):
        # complete_video_features
        print("-----------------------------------------------")

        print("bandwidth =" + str(bandwidth))
        normalized_mean_shift_output_file = "./clustering_results/mean_shift/complete_video/" \
                                            + str(bandwidth) + "_mean_shift.csv"
        input_video_features_cm.mean_shift(bandwidth, normalized_mean_shift_output_file)
        bandwidth += 5


def main():
    print "1 = k_means"
    print "2 = db_scan"
    print "3 = birch"
    print "4 = mean_shift"
    input_option = raw_input("Enter your input:")

    if input_option == "1":
        print "1 = k_means"
        run_k_means()
    if input_option == "2":
        print "2 = db_scan"
        run_db_scan()
    if input_option == "3":
        print "3 = birch"
        run_birch()
    if input_option == "4":
        print "4 = mean_shift"
        run_mean_shift()


main()
