import utility as utl
import csv
from random import randrange


class Video:
    name = ""
    category = ""
    shots = {}

    def __init__(self):
        pass


class Shot:
    number = 0
    features = []

    def __init__(self):
        pass


class K_Medoids:
    def __init__(self, directory_path, input_file_name, out_put_file_name):
        self.__file_name = input_file_name
        self.__directory_path = directory_path
        self.__out_put_file_name = out_put_file_name
        self.__file_path = directory_path + input_file_name
        self.__video_list = K_Medoids.__fill_video_list(self.__file_path)
        print(str(len(self.__video_list)))

    @staticmethod
    def __convert_to_float(string_vector):
        vector = []
        for item in string_vector:
            vector.append(float(item))
        return vector

    @staticmethod
    def __fill_video_list(csv_file):
        with open(csv_file) as f:
            data_set_count = sum(1 for line in f) - 1
        f.close()
        with open(csv_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            iteration = 0
            video_list = []
            print("preparing video list data ...")
            video = Video()

            for row in reader:
                if iteration > 0:
                    video_name = row[0]
                    shot_number = row[1]
                    category_label = row[2]
                    features = row[3:len(row)]
                    if video.name == "":
                        video.category = category_label
                        video.name = video_name
                        video.clusters = {}
                        video.shots = {}
                    shot = Shot()
                    shot.features = K_Medoids.__convert_to_float(features)
                    shot.number = int(shot_number)
                    video.shots[shot_number] = shot

                    if video.name != video_name:
                        video_list.append(video)
                        video = Video()
                        video.category = category_label
                        video.name = video_name
                        video.clusters = {}
                        video.shots = {}

                    utl.print_progress_bar(iteration + 1, data_set_count)
                iteration += 1
        csvFile.close()
        print("")
        return video_list

    @staticmethod
    def __get_video_shots(video):
        shots = []
        for shot_number, features in video.shots.iteritems():
            shots.append(int(shot_number))
        shots.sort()
        return shots

    @staticmethod
    def __generate_full_distance_matrix(video1, video2):
        v1_shot_numbers = K_Medoids.__get_video_shots(video1)
        v2_shots_numbers = K_Medoids.__get_video_shots(video2)
        row_count = len(v1_shot_numbers)
        column_count = len(v2_shots_numbers)
        matrix = []
        for v1_shot_number in v1_shot_numbers:
            row = []
            for v2_shot_number in v2_shots_numbers:
                v1_shot = video1.shots[str(v1_shot_number)]
                v2_shot = video2.shots[str(v2_shot_number)]
                distance = utl.calculate_distance(v1_shot.features, v2_shot.features)
                row.append(distance)
            matrix.append(row)
        return matrix, row_count, column_count

    @staticmethod
    def __convert_to_linear_array(array_2d):
        linear_array = []
        row_number = len(array_2d)
        col_number = len(array_2d[0])
        for row in range(row_number):
            for col in range(col_number):
                linear_array.append([row, col, array_2d[row][col]])
        return linear_array

    @staticmethod
    def __calculate_distance(video1, video2):
        # 1- creat 2 dimensional array
        #    row = v1 shots
        #    col = v2 shots
        # 2- fill the matrix as the following
        #       calculate distance
        # 3- for each element that is not belong to removed col or row:
        #       search for the smallest value and remove the col and row
        distance_matrix, row_count, column_count = K_Medoids.__generate_full_distance_matrix(video1, video2)

        linear_array = K_Medoids.__convert_to_linear_array(distance_matrix)
        linear_array.sort(key=lambda x: x[2])
        removed_columns = []
        removed_rows = []
        distance_score = 0
        # phase 1
        for elem in linear_array:
            row = elem[0]
            col = elem[1]
            distance = elem[2]
            if row not in removed_rows and col not in removed_columns:
                removed_columns.append(col)
                removed_rows.append(row)
                if distance != 0:
                    distance_score += distance
        miss_calculated_rows = []
        miss_calculated_columns = []
        for row in range(row_count):
            if row not in removed_rows:
                miss_calculated_rows.append(row)

        for row in miss_calculated_rows:
            distance_score += min(distance_matrix[row])

        # special case solve it

        for col in range(column_count):
            if col not in removed_columns:
                miss_calculated_columns.append(col)
        for col in miss_calculated_columns:
            complete_column = []
            for row in range(row_count):
                complete_column.append(distance_matrix[row][col])
            distance_score += min(complete_column)
        return distance_score

    def run(self, n_cluster=2):
        # 1- select k random point as initial cluster centroid
        # 2- for each video select cluster
        # 3- recalculate the centroids in each cluster
        # 4- repeat step 2 and 3

        # 1- select k random point as initial cluster centroid
        centroids_indexes = []
        for k in range(n_cluster):
            centroid = randrange(len(self.__video_list))
            while centroid in centroids_indexes:
                centroid = randrange(len(self.__video_list))
            centroids_indexes.append(centroid)

        # 2- for each video select cluster
        k_result = {}
        for k in range(n_cluster):
            k_result = []
        for video in self.__video_list:
            centroid_distances = []
            for k in range(n_cluster):
                ci = centroids_indexes[k]
                cluster_centroid = self.__video_list[ci]
                distance = K_Medoids.__calculate_distance(video, cluster_centroid)
                centroid_distances.append(distance)

            # get video cluster
            video_cluster = centroid_distances.index(min(centroid_distances))
            # save the video in cluster dictionary
            k_result[video_cluster].append(video)

        print ""


def main():
    directory = "./"
    input_file = "shot_features_test.csv"
    output_file = "_video_similarity.csv"
    methods = ["shots_method", "common_clusters_method", "distance_matrix_method"]
    method = methods[2]
    k_medoids = K_Medoids(directory, input_file, method + output_file)
    k_medoids.run(2)
    print "Done!"


main()
