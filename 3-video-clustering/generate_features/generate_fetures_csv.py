import utility
import csv
from feature_manager import FeatureManager

directory_path = "C:/features/structure-analysis-shots/"
feature_files = utility.get_file_name_list(directory_path)
feature_vector_list = []
iteration = 1
max_value = len(feature_files)
for file_name in feature_files:
    fm = FeatureManager(directory_path, file_name)
    feature_vector_list = feature_vector_list + fm.get_feature_vector_list()
    utility.print_progress_bar(iteration, max_value)
    iteration += 1
print "start csv"
with open('shots_features.csv', 'wb') as f:
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
    max_value = len(feature_vector_list)
    for vector in feature_vector_list:
        the_writer.writerow(vector)
        utility.print_progress_bar(iteration, max_value)
        iteration += 1
    f.close()
