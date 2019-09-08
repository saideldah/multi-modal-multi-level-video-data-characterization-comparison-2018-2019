import utility as utl
import csv


class VideoClusterResult:
    name = ""
    shot = {}
    category = ""

    def __init__(self):
        pass


class VideoFeatures:
    name = ""
    shot = {}
    category = ""

    def __init__(self):
        pass


def fill_clustering_results_data(clustering_results_file_path):
    with open(clustering_results_file_path) as f:
        data_set_count = sum(1 for line in f) - 1
    f.close()
    with open(clustering_results_file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        iteration = 0
        video_list = {}
        print("preparing clustering results data ...")
        video_cluster_result = VideoClusterResult()

        for row in reader:
            if iteration > 0:
                video_name = row[0]
                shot_number = row[1]
                category_label = row[2]
                cluster_label = row[3]
                if video_cluster_result.name == "":
                    video_cluster_result.category = category_label
                    video_cluster_result.name = video_name
                    video_cluster_result.shot = {}

                video_cluster_result.shot[shot_number] = cluster_label

                if video_cluster_result.name != video_name and video_cluster_result.name not in video_list:
                    video_list[video_cluster_result.name] = video_cluster_result
                    video_cluster_result = VideoClusterResult()
                    video_cluster_result.category = category_label
                    video_cluster_result.name = video_name
                    video_cluster_result.shot = {}

                utl.print_progress_bar(iteration + 1, data_set_count)
            iteration += 1
    csvFile.close()
    print("")
    return video_list


def fill_features_data(features_file_path):
    with open(features_file_path) as f:
        data_set_count = sum(1 for line in f) - 1
    f.close()
    with open(features_file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        iteration = 0
        video_list = {}
        print("preparing clustering results data ...")
        video = VideoClusterResult()

        for row in reader:
            if iteration > 0:
                video_name = row[0]
                shot_number = row[1]
                category_label = row[2]
                features = row[3:len(row)]
                if video.name == "":
                    video.category = category_label
                    video.name = video_name
                    video.shot = {}

                video.shot[shot_number] = features

                if video.name != video_name and video.name not in video_list:
                    video_list[video.name] = video
                    video = VideoClusterResult()
                    video.category = category_label
                    video.name = video_name
                    video.shot = {}

                utl.print_progress_bar(iteration + 1, data_set_count)
            iteration += 1
    csvFile.close()
    print("")
    return video_list


def merge_features_with_clustering_results_not_normalized(features_file_path, clustering_results_file_path,
                                                          out_put_file_path):
    clustering_result_data = fill_clustering_results_data(clustering_results_file_path)
    features_data = fill_features_data(features_file_path)
    print "creating csv file..."
    with open(out_put_file_path, 'wb') as f:
        the_writer = csv.writer(f)
        headers = [
            "video",
            "shot_number",
            "category",
            "cluster",
            "interactions_number_speakers_2",
            "interactions_number_speakers_3",
            "interactions_number_speakers_4",
            "interactions_number_speakers_4+",
            "intervention_short",
            "intervention_long",
            "speakers_type_ponctuel",
            "speakers_type_localise",
            "speakers_type_present",
            "speakers_type_regulier",
            "speakers_type_important",
            "speaker_distribution",
            "mean_number_of_faces",
            "std_number_of_faces",
            "inter_intensity_variation1",
            "inter_intensity_variation2",
            "inter_intensity_variation3",
            "inter_intensity_variation4",
            "inter_intensity_variation5",
            "inter_intensity_variation6",
            "inter_intensity_variation7",
            "inter_intensity_variation8",
            "inter_intensity_variation9",
            "intra_intensity_variation1",
            "intra_intensity_variation2",
            "intra_intensity_variation3",
            "intra_intensity_variation4",
            "intra_intensity_variation5",
            "intra_intensity_variation6",
            "intra_intensity_variation7",
            "intra_intensity_variation8",
            "intra_intensity_variation9",
            "number_shot_transition",
            "number_speaker_transition",
            "speech",
            "music",
            "speech_with_music",
            "speech_with_non_music",
            "non_speech_with_music",
            "non_speech_with_non_music",
            "words",
            "duration"
        ]
        the_writer.writerow(headers)
        video_list_length = len(clustering_result_data)
        max_value = video_list_length
        iteration = 1
        for video_name, video in clustering_result_data.iteritems():
            video_from_features = features_data[video_name]
            for shot_number, cluster in video.shot.iteritems():
                features = video_from_features.shot[shot_number]
                vector = [video_name, shot_number, video.category, cluster] + features
                the_writer.writerow(vector)
            utl.print_progress_bar(iteration, max_value)
            iteration += 1
        f.close()
        print("")
        print("csv file has been created successfully")


def merge_features_with_clustering_results_normalized(features_file_path, clustering_results_file_path,
                                                      out_put_file_path):
    clustering_result_data = fill_clustering_results_data(clustering_results_file_path)
    features_data = fill_features_data(features_file_path)
    print "creating csv file..."
    with open(out_put_file_path, 'wb') as f:
        the_writer = csv.writer(f)
        headers = [
            "video",
            "shot_number",
            "category",
            "cluster",
            "interactions_number_speakers_2",
            "interactions_number_speakers_3",
            "interactions_number_speakers_4",
            "interactions_number_speakers_4+",
            "intervention_short",
            "intervention_long",
            "speakers_type_ponctuel",
            "speakers_type_localise",
            "speakers_type_present",
            "speakers_type_regulier",
            "speakers_type_important",
            "speaker_distribution",
            "mean_number_of_faces",
            "std_number_of_faces",
            "inter_intensity_variation",
            "intra_intensity_variation",
            "number_shot_transition",
            "number_speaker_transition",
            "speech",
            "music",
            "speech_with_music",
            "speech_with_non_music",
            "non_speech_with_music",
            "non_speech_with_non_music",
            "words",
            "duration"
        ]
        the_writer.writerow(headers)
        video_list_length = len(clustering_result_data)
        max_value = video_list_length
        iteration = 1
        for video_name, video in clustering_result_data.iteritems():
            video_from_features = features_data[video_name]
            for shot_number, cluster in video.shot.iteritems():
                features = video_from_features.shot[shot_number]
                vector = [video_name, shot_number, video.category, cluster] + features
                the_writer.writerow(vector)
            utl.print_progress_bar(iteration, max_value)
            iteration += 1
        f.close()
        print("")
        print("csv file has been created successfully")


def generate_shot_merged_files_not_normalized():
    features_file_path = "./features/shot_features.csv"
    clustering_results_file_path = "./clustering_results/kMeans/shot/complete-intra-inter/"
    output_file_path = "./mean-average-precision/kMeans/shot/complete-intra-inter/merged-with-features/"
    clustering_results_file_name_list = utl.get_file_name_list(clustering_results_file_path)

    for clustering_result_file_name in clustering_results_file_name_list:
        if clustering_result_file_name != "merged-with-features":
            print ("generating " + clustering_result_file_name)
            merge_features_with_clustering_results_not_normalized(features_file_path,
                                                                  clustering_results_file_path + clustering_result_file_name
                                                                  , output_file_path + clustering_result_file_name)
            print ("---------------------------------------------------------------")


def generate_shot_merged_files_normalized():
    features_file_path = "./features/normalized_shot_features.csv"
    clustering_results_file_path = "./clustering_results/kMeans/shot/normalized-intra-inter/"
    output_file_path = "./mean-average-precision/kMeans/shot/normalized-intra-inter/merged-with-features/"
    clustering_results_file_name_list = utl.get_file_name_list(clustering_results_file_path)

    for clustering_result_file_name in clustering_results_file_name_list:
        if clustering_result_file_name != "merged-with-features":
            print ("generating " + clustering_result_file_name)
            merge_features_with_clustering_results_normalized(features_file_path,
                                                              clustering_results_file_path + clustering_result_file_name
                                                              , output_file_path + clustering_result_file_name)
            print ("---------------------------------------------------------------")


def generate_video_merged_files_not_normalized():
    features_file_path = "./features/video_features.csv"
    clustering_results_file_path = "./clustering_results/kMeans/video/complete-intra-inter/"
    output_file_path = "./mean-average-precision/kMeans/video/complete-intra-inter/merged-with-features/"
    clustering_results_file_name_list = utl.get_file_name_list(clustering_results_file_path)

    for clustering_result_file_name in clustering_results_file_name_list:
        if clustering_result_file_name != "merged-with-features":
            print ("generating " + clustering_result_file_name)
            merge_features_with_clustering_results_not_normalized(features_file_path,
                                                                  clustering_results_file_path + clustering_result_file_name
                                                                  , output_file_path + clustering_result_file_name)
            print ("---------------------------------------------------------------")


def generate_video_merged_files_normalized():
    features_file_path = "./features/normalized_video_features.csv"
    clustering_results_file_path = "./clustering_results/kMeans/video/normalized-intra-inter/"
    output_file_path = "./mean-average-precision/kMeans/video/normalized-intra-inter/merged-with-features/"
    clustering_results_file_name_list = utl.get_file_name_list(clustering_results_file_path)

    for clustering_result_file_name in clustering_results_file_name_list:
        if clustering_result_file_name != "merged-with-features":
            print ("generating " + clustering_result_file_name)
            merge_features_with_clustering_results_normalized(features_file_path,
                                                              clustering_results_file_path + clustering_result_file_name
                                                              , output_file_path + clustering_result_file_name)
            print ("---------------------------------------------------------------")


def generate_complete_video_merged_files_not_normalized():
    features_file_path = "./features/complete_video_features.csv"
    clustering_results_file_path = "./clustering_results/kMeans/video/complete-intra-inter/"
    output_file_path = "./mean-average-precision/kMeans/video/complete-intra-inter/merged-with-features/"
    clustering_results_file_name_list = utl.get_file_name_list(clustering_results_file_path)

    for clustering_result_file_name in clustering_results_file_name_list:
        if clustering_result_file_name != "merged-with-features":
            print ("generating " + clustering_result_file_name)
            merge_features_with_clustering_results_not_normalized(features_file_path,
                                                                  clustering_results_file_path + clustering_result_file_name
                                                                  , output_file_path + clustering_result_file_name)
            print ("---------------------------------------------------------------")


def generate_complete_video_merged_files_normalized():
    features_file_path = "./features/normalized_complete_video_features.csv"
    clustering_results_file_path = "./clustering_results/kMeans/video/normalized-intra-inter/"
    output_file_path = "./mean-average-precision/kMeans/video/normalized-intra-inter/merged-with-features/"
    clustering_results_file_name_list = utl.get_file_name_list(clustering_results_file_path)

    for clustering_result_file_name in clustering_results_file_name_list:
        if clustering_result_file_name != "merged-with-features":
            print ("generating " + clustering_result_file_name)
            merge_features_with_clustering_results_normalized(features_file_path,
                                                              clustering_results_file_path + clustering_result_file_name
                                                              , output_file_path + clustering_result_file_name)
            print ("---------------------------------------------------------------")


def main():
    generate_shot_merged_files_not_normalized()
    generate_video_merged_files_not_normalized()
    generate_shot_merged_files_normalized()
    generate_video_merged_files_normalized()
    generate_complete_video_merged_files_not_normalized()
    generate_complete_video_merged_files_normalized()


main()
