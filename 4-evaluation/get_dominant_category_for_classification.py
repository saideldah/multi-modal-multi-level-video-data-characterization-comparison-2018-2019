import utility

input_file = "./classification_results/Dev_Features_Shots_Normalized_CV10_Output_final.tsv"
output_file = "./classification_results/Dev_Features_Shots_Normalized_CV10_Output_final.csv"

utility.tsc_to_csv(input_file, output_file)
