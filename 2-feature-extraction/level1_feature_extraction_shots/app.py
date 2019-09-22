import combineLowLevelFeatures as combineLowLevelFeatures
import utility

input_directory_path = "C:/code/features/input/structure_analysis/test/4/"
output_directory_path = "C:/code/features/output/shots/structure-analysis-shots-test/"
shots_directory_path = "C:/code/features/input/shots_files/test_normalized/"

shot_file_name_list = utility.get_file_name_list(shots_directory_path)
generated_files = utility.get_file_name_list(output_directory_path)
feature_files = utility.get_file_name_list(input_directory_path)
print input_directory_path

i = 1
l = len(feature_files)
for shot_file_name in shot_file_name_list:
    shot_list = utility.get_shots(shots_directory_path + shot_file_name)
    if len(shot_list) > 0 and shot_file_name not in generated_files and shot_file_name in feature_files:
        input_file_path = input_directory_path + shot_file_name
        output_file_path = output_directory_path + shot_file_name
        combineLowLevelFeatures.generate_percentage_descriptors(input_file_path, output_file_path, shot_list)
        utility.print_progress_bar(i, l)
        i += 1

