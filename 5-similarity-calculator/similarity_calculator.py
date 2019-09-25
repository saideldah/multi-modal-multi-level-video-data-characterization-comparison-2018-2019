import utility as utl
import csv


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


class SimilarityCalculator:
    def __init__(self, directory_path, input_file_name, out_put_file_name):
        self.__file_name = input_file_name
        self.__directory_path = directory_path
        self.__out_put_file_name = out_put_file_name
        self.__file_path = directory_path + input_file_name
        self.__video_list = SimilarityCalculator.__fill_video_list(self.__file_path)

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
                    shot.features = SimilarityCalculator.__convert_to_float(features)
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
    def __get_video_cluster_labels(video):
        clusters_labels = []
        for cluster_label, number_of_shots_per_cluster in video.clusters.iteritems():
            clusters_labels.append(cluster_label)
        return clusters_labels

    @staticmethod
    def __get_video_number_of_shots(video):
        shot_counter = 0
        for cluster_label, number_of_shots_per_cluster in video.clusters.iteritems():
            shot_counter += number_of_shots_per_cluster
        return shot_counter

    @staticmethod
    def __get_common_union(video1, video2):
        v1_clusters_labels = SimilarityCalculator.__get_video_cluster_labels(video1)
        v2_clusters_labels = SimilarityCalculator.__get_video_cluster_labels(video2)
        clusters_union = set(v1_clusters_labels + v2_clusters_labels)
        return clusters_union

    @staticmethod
    def __get_clusters_intersection(video1, video2):
        v1_clusters_labels = SimilarityCalculator.__get_video_cluster_labels(video1)
        v2_clusters_labels = SimilarityCalculator.__get_video_cluster_labels(video2)
        clusters_intersection = list(set(v1_clusters_labels) & set(v2_clusters_labels))
        return clusters_intersection

    @staticmethod
    def __get_number_of_video_shots_for_common_clusters(video, common_clusters):
        score = 0
        # for each common cluster get number of shots
        # example c1 and c2 are common, c1 contains 5 shots and c2 contains 6 shots
        # the score is 11
        for cluster_label, number_of_shots_per_cluster in video.clusters.iteritems():
            if cluster_label in common_clusters:
                score += number_of_shots_per_cluster
        return score

    @staticmethod
    def __calculate_similarity_common_shots_method(video1, video2):
        common_clusters = SimilarityCalculator.__get_clusters_intersection(video1, video2)
        v1_score = float(SimilarityCalculator.__get_number_of_video_shots_for_common_clusters(video1, common_clusters))
        v2_score = float(SimilarityCalculator.__get_number_of_video_shots_for_common_clusters(video2, common_clusters))
        v1_total_shot_count = float(SimilarityCalculator.__get_video_number_of_shots(video1))
        v2_total_shot_count = float(SimilarityCalculator.__get_video_number_of_shots(video2))
        similarity_score = (v1_score + v2_score) / (v1_total_shot_count + v2_total_shot_count)
        return similarity_score

    @staticmethod
    def __calculate_similarity_common_clusters_method(video1, video2):
        # common clusters/ number of all clusters
        clusters_intersection = SimilarityCalculator.__get_clusters_intersection(video1, video2)
        clusters_union = SimilarityCalculator.__get_common_union(video1, video2)
        similarity_score = float(len(clusters_intersection)) / float(len(clusters_union))
        return similarity_score

    @staticmethod
    def __get_video_shots(video):
        shots = []
        for shot_number, features in video.shots.iteritems():
            shots.append(int(shot_number))
        shots.sort()
        return shots

    @staticmethod
    def __generate_distance_matrix(video1, video2):
        v1_shot_numbers = SimilarityCalculator.__get_video_shots(video1)
        v2_shots_numbers = SimilarityCalculator.__get_video_shots(video2)
        row_count = len(v1_shot_numbers)
        column_count = len(v2_shots_numbers)
        matrix = []
        for v1_shot_number in v1_shot_numbers:
            row = []
            for v2_shot_number in v2_shots_numbers:
                v1_shot = video1.shots[str(v1_shot_number)]
                v2_shot = video2.shots[str(v2_shot_number)]
                distance = 0
                if v1_shot.cluster != v2_shot.cluster:
                    distance = utl.calculate_distance(v1_shot.features, v2_shot.features)
                row.append(distance)
            matrix.append(row)
        return matrix, row_count, column_count

    @staticmethod
    def __generate_full_distance_matrix(video1, video2):
        v1_shot_numbers = SimilarityCalculator.__get_video_shots(video1)
        v2_shots_numbers = SimilarityCalculator.__get_video_shots(video2)
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
    def __get_audio_features(features):
        return features[0:12]

    @staticmethod
    def __get_video_features(features):
        return features[12:len(features)]

    @staticmethod
    def __generate_distance_matrix_on_separate_features(video1, video2):
        v1_shot_numbers = SimilarityCalculator.__get_video_shots(video1)
        v2_shot_numbers = SimilarityCalculator.__get_video_shots(video2)
        matrix = []
        for v1_shot_number in v1_shot_numbers:
            row = []
            for v2_shot_number in v2_shot_numbers:
                v1_shot = video1.shots[str(v1_shot_number)]
                v2_shot = video2.shots[str(v2_shot_number)]
                distance = 0
                if v1_shot.cluster != v2_shot.cluster:
                    v1_audio_features = SimilarityCalculator.__get_audio_features(v1_shot.features)
                    v1_video_features = SimilarityCalculator.__get_audio_features(v1_shot.features)

                    v2_audio_features = SimilarityCalculator.__get_audio_features(v2_shot.features)
                    v2_video_features = SimilarityCalculator.__get_audio_features(v2_shot.features)

                    audio_distance = utl.calculate_distance(v1_audio_features, v2_audio_features)
                    video_distance = utl.calculate_distance(v1_video_features, v2_video_features)

                    distance = 0.5 * (audio_distance + video_distance)
                row.append(distance)
            matrix.append(row)
        return matrix

    @staticmethod
    def convert_to_linear_array(array_2d):
        linear_array = []
        row_number = len(array_2d)
        col_number = len(array_2d[0])
        for row in range(row_number):
            for col in range(col_number):
                linear_array.append([row, col, array_2d[row][col]])
        return linear_array

    @staticmethod
    def __calculate_similarity_distance_matrix_method(video1, video2):
        # 1- creat 2 dimensional array
        #    row = v1 shots
        #    col = v2 shots
        # 2- fill the matrix as the following
        #       if complete_video is in common cluster then 0
        #       else calculate distance
        # 3- for each zero that is not in removed col and row, remove the col and row
        #   for each element that is not belong to removed col or row:
        #       search for the smallest value and remove the col and row
        distance_matrix = SimilarityCalculator.__generate_distance_matrix(video1, video2)
        linear_array = SimilarityCalculator.convert_to_linear_array(distance_matrix)
        linear_array.sort(key=lambda x: x[2])
        removed_columns = []
        removed_rows = []
        distance_score = 0
        for elem in linear_array:
            row = elem[0]
            col = elem[1]
            distance = elem[2]
            if row not in removed_rows and col not in removed_columns:
                removed_columns.append(col)
                removed_rows.append(row)
                if distance != 0:
                    distance_score += distance
        return distance_score

    @staticmethod
    def __calculate_similarity_distance_matrix_method_v2(video1, video2):
        # 1- creat 2 dimensional array
        #    row = v1 shots
        #    col = v2 shots
        # 2- fill the matrix as the following
        #       calculate distance
        # 3- for each element that is not belong to removed col or row:
        #       search for the smallest value and remove the col and row
        distance_matrix, row_count, column_count = SimilarityCalculator.__generate_full_distance_matrix(video1, video2)

        linear_array = SimilarityCalculator.convert_to_linear_array(distance_matrix)
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

    def generate_video_similarity_distance_csv(self, method):

        methods = {"shots_method": self.__calculate_similarity_common_shots_method,
                   "common_clusters_method": self.__calculate_similarity_common_clusters_method,
                   "distance_matrix_method": self.__calculate_similarity_distance_matrix_method_v2}
        print "creating csv file..."
        with open(self.__directory_path + self.__out_put_file_name, 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "v1",
                "v2",
                "v1 category",
                "v2 category",
                "distance"
            ]
            the_writer.writerow(headers)
            video_list_length = len(self.__video_list)
            max_value = video_list_length
            max_value = 20
            iteration = 1

            for i in range(video_list_length):
                # print("calculate distance for " + self.__video_list[i].name)
                # print ""
                # iteration = 1
                for j in range(i + 1, video_list_length):
                    v1 = self.__video_list[i]
                    v2 = self.__video_list[j]
                    video_similarity_row = [v1.name, v2.name, v1.category, v2.category]

                    distance = methods[method](v1, v2)
                    video_similarity_row.append(distance)
                    the_writer.writerow(video_similarity_row)
                utl.print_progress_bar(iteration, max_value)
                iteration += 1
                if iteration > max_value:
                    break
                # print ""
            f.close()
            print("")
            print("csv file has been created successfully")


def main():
    directory = "./"
    input_file = "shot_features.csv"
    output_file = "_video_similarity.csv"
    methods = ["shots_method", "common_clusters_method", "distance_matrix_method"]
    method = methods[2]
    similarity_calculator = SimilarityCalculator(directory, input_file, method + output_file)
    similarity_calculator.generate_video_similarity_distance_csv(method)
    print "Done!"


main()
