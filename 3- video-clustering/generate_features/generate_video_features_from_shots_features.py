# in this file we will generate feature set by taking the average of shot feature for each video

import utility as utl
import csv


class Video:
    name = ""
    shots = {}
    category = ""
    features = []

    def __init__(self):
        pass


def calculate_vectors_average(vectors):
    result = [0] * len(vectors[0])
    total_vectors = len(vectors)
    for vector in vectors:
        result = map(sum, zip(vector, result))
    for i in range(0, len(result)):
        result[i] = result[i] / total_vectors
    return result


def convert_to_float(string_vector):
    vector = []
    for item in string_vector:
        vector.append(float(item))
    return vector


def fill_features_data(features_file_path):
    with open(features_file_path) as f:
        data_set_count = sum(1 for line in f) - 1
    f.close()
    with open(features_file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        iteration = 0
        video_list = []
        print("preparing clustering results data ...")
        video = Video()

        for row in reader:
            if iteration > 0:
                video_name = row[0]
                shot_number = row[1]
                category_label = row[2]
                features = convert_to_float(row[3:len(row)])
                if video.name == "":
                    video.category = category_label
                    video.name = video_name
                    video.shots = {}

                video.shots[shot_number] = features

                if video.name != video_name and video.name not in video_list:
                    shot_feature_list = []
                    for shot, shot_features in video.shots.iteritems():
                        shot_feature_list.append(shot_features)
                    video.features = calculate_vectors_average(shot_feature_list)
                    video_list.append(video)
                    # new video
                    video = Video()
                    video.category = category_label
                    video.name = video_name
                    video.shots = {}
                    video.features = []

                utl.print_progress_bar(iteration + 1, data_set_count)
            iteration += 1
    csvFile.close()
    print("")
    return video_list


def generate_video_feature_set_csv(input_file_path, output_file_path):
    video_list = fill_features_data(input_file_path)
    print "start csv"
    with open(output_file_path, 'wb') as f:
        the_writer = csv.writer(f)
        headers = [
            "video",
            "shot_count",
            "category",
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
        iteration = 1
        max_value = len(video_list)
        for video in video_list:
            vector = [video.name, len(video.shots), video.category] + video.features
            the_writer.writerow(vector)
            utl.print_progress_bar(iteration, max_value)
            iteration += 1
        f.close()


def main():
    input_file_path = "../shots_features.csv"
    output_file_path = "../video_features.csv"
    generate_video_feature_set_csv(input_file_path, output_file_path)


main()
