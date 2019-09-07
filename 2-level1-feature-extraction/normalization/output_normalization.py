# max_shot_duration: 11367.0
# max_shot_word_length: 7640
# 255
import utility

output_directory_path = "C:/features/structure-analysis-shots-test/"
output_file_name_list = utility.get_file_name_list(output_directory_path)

max_shot_duration = 0
max_shot_word_length = 0
i = 0
l = len(output_file_name_list)
for file_name in output_file_name_list:
    i = i + 1
    utility.print_progress_bar(i, l)

