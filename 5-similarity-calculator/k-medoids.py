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
        self.__distance_memory = {}
        print("number of videos = " + str(len(self.__video_list)))

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

    def __get_video_with_minimum_distance_sum(self, video_list):
        video_distance_sum = {}
        video_list_count = len(video_list)
        for v1_index in range(video_list_count):
            video_distance_sum[v1_index] = 0
            for v2_index in range(v1_index + 1, video_list_count):
                video1 = video_list[v1_index]
                video2 = video_list[v2_index]
                if video1.name == video2.name:
                    continue
                key = video1.name + "_" + video2.name
                kei_inverse = video2.name + "_" + video1.name
                if key not in self.__distance_memory or not kei_inverse not in self.__distance_memory:
                    distance = K_Medoids.__calculate_distance(video1, video2)
                    self.__distance_memory[key] = distance
                video_distance_sum[v1_index] += self.__distance_memory[key]
        video_with_minimum_distance_sum_index = min(video_distance_sum, key=video_distance_sum.get)
        video_with_minimum_distance_sum = video_list[video_with_minimum_distance_sum_index]
        return video_with_minimum_distance_sum

    def run(self, n_cluster=2, n_phases=20):
        print ("Start K_Medoids")
        print ("number of clusters: " + str(n_cluster))

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
            k_result[k] = []
        for video in self.__video_list:
            centroid_distances = []
            for k in range(n_cluster):
                ci = centroids_indexes[k]
                cluster_centroid = self.__video_list[ci]
                key = video.name + "_" + cluster_centroid.name
                kei_inverse = cluster_centroid.name + "_" + video.name
                if key not in self.__distance_memory or not kei_inverse not in self.__distance_memory:
                    distance = K_Medoids.__calculate_distance(video, cluster_centroid)
                    self.__distance_memory[key] = distance
                distance = self.__distance_memory[key]
                centroid_distances.append(distance)
            # get video cluster
            video_cluster = centroid_distances.index(min(centroid_distances))
            # save the video in cluster dictionary
            k_result[video_cluster].append(video)

        # 3- recalculate the centroids in each cluster
        # calculate distance between each video in tha same cluster
        # sum the distances of each video
        # ths video with minimum sum will be the new center
        for i in range(n_phases):
            print ("phase: " + str(i + 1) + "/" + str(n_phases))
            new_centroid_list = {}
            for cluster, cluster_video_list in k_result.iteritems():
                new_centroid_list[cluster] = self.__get_video_with_minimum_distance_sum(cluster_video_list)

            k_result = {}
            for k in range(n_cluster):
                k_result[k] = []
            for video in self.__video_list:
                centroid_distances = {}
                for cluster, cluster_centroid in new_centroid_list.iteritems():
                    key = video.name + "_" + cluster_centroid.name
                    kei_inverse = cluster_centroid.name + "_" + video.name
                    if key not in self.__distance_memory or not kei_inverse not in self.__distance_memory:
                        distance = K_Medoids.__calculate_distance(video, cluster_centroid)
                        self.__distance_memory[key] = distance
                    distance = self.__distance_memory[key]
                    centroid_distances[cluster] = distance

                # get video cluster
                video_cluster = min(centroid_distances, key=centroid_distances.get)
                # save the video in cluster dictionary
                k_result[video_cluster].append(video)

        return k_result


def generate_csv(k_medoids_result, output_file):
    print "generating generate category feature csv"
    with open(output_file, 'wb') as f:
        the_writer = csv.writer(f)
        headers = [
            "video",
            "category",
            "cluster"
        ]
        the_writer.writerow(headers)
        iteration = 1
        max_value = len(k_medoids_result)
        for cluster, cluster_videos in k_medoids_result.iteritems():
            for video in cluster_videos:
                vector = [video.name, video.category, cluster]
                the_writer.writerow(vector)
            utl.print_progress_bar(iteration, max_value)
            iteration += 1
        f.close()


def main():
    directory = "./"
    input_file = "shot_features_test.csv"
    output_file = "k_medoids_results_20.csv"
    k_medoids = K_Medoids(directory, input_file, output_file)
    k_medoids_result = k_medoids.run(20)
    generate_csv(k_medoids_result, output_file)
    print "Done!"


main()
