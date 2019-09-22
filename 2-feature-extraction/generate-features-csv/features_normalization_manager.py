import csv

import utility


class FeaturesNormalizationManager:

    def __init__(self, directory_path, file_name):
        self.features_file_path = directory_path + file_name
        self.feature_list = FeaturesNormalizationManager.__fill_features_data(self.features_file_path)
        pass

    @staticmethod
    def __fill_features_data(features_file_path):

        with open(features_file_path) as f:
            data_set_count = sum(1 for line in f) - 1
        f.close()
        with open(features_file_path, 'r') as csvFile:
            reader = csv.reader(csvFile)
            iteration = 0
            print("preparing clustering results data ...")
            feature_list = []
            for row in reader:
                if iteration > 0:
                    feature_list.append(row)
                    utility.print_progress_bar(iteration + 1, data_set_count)
                iteration += 1
        csvFile.close()
        print("")
        return feature_list

    @staticmethod
    def __convert_to_float(string_vector):
        vector = []
        for item in string_vector:
            vector.append(float(item))
        return vector

    # Processing for the features, get the average of intra and inter (one value per intra and one value per inter)
    def generate_normalized_feature_csv(self):
        print "start csv"
        with open('normalized_complete_video_features.csv', 'wb') as f:
            the_writer = csv.writer(f)
            headers = [
                "video",
                "shot_number",
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
            iteration = 1
            max_value = len(self.feature_list)
            for vector in self.feature_list:
                normalized_vector = vector[0:17]
                inter_intensity_variation_vector = self.__convert_to_float(vector[17:26])
                inter_intensity_variation = sum(inter_intensity_variation_vector) / len(
                    inter_intensity_variation_vector)
                intra_intensity_variation_vector = self.__convert_to_float(vector[26:35])
                intra_intensity_variation = sum(intra_intensity_variation_vector) / len(
                    intra_intensity_variation_vector)
                other_features = self.__convert_to_float(vector[35:len(vector)])
                normalized_vector.append(inter_intensity_variation)
                normalized_vector.append(intra_intensity_variation)
                normalized_vector += other_features
                the_writer.writerow(normalized_vector)
                utility.print_progress_bar(iteration, max_value)
                iteration += 1
            f.close()


features_file_path = "complete_video_features.csv"
directory_path = "./"

features_normalization_manager = FeaturesNormalizationManager(directory_path, features_file_path)
features_normalization_manager.generate_normalized_feature_csv()
