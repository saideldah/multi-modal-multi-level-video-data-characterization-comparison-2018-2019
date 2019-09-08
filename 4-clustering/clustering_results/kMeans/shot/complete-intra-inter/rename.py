import utility
import os

folders = [
    "./videos/normalized-intra-inter/category-per-cluster/",
    "./videos/normalized-intra-inter/cluster-per-category/",
    "./videos/normalized-intra-inter/merged-with-features/",
    "./videos/complete-intra-inter/category-per-cluster/",
    "./videos/complete-intra-inter/cluster-per-category/",
    "./videos/complete-intra-inter/merged-with-features/",
    "./shots/normalized-intra-inter/category-per-cluster/",
    "./shots/normalized-intra-inter/cluster-per-category/",
    "./shots/normalized-intra-inter/merged-with-features/",
    "./shots/complete-intra-inter/category-per-cluster/",
    "./shots/complete-intra-inter/cluster-per-category/",
    "./shots/complete-intra-inter/merged-with-features/"
]

substring_to_remove_list = [
    "_video_clustering_results_category_distribution_per_cluster_mean_average_precision_category_per_cluster"
    , "_shot_clustering_results_category_distribution_per_cluster_mean_average_precision_category_per_cluster"
    , "_shot_clustering_results_category_distribution_per_cluster"
    , "_shot_clustering_results_cluster_distribution_per_category"
    , "_video_clustering_results_category_distribution_per_cluster"
    , "_video_clustering_results_cluster_distribution_per_category"
    , "_cluster_distribution_per_category"
    , "_category_distribution_per_cluster"
    , "_shots_clustering_results"
    , "_video_clustering_results"
]


def rename(f_name=""):
    for substring_to_remove in substring_to_remove_list:
        f_name = f_name.replace(substring_to_remove, "")
    return f_name


def rename_file(directory, old_name, new_name):
    old_file = os.path.join(directory, old_name)
    new_file = os.path.join(directory, new_name)
    os.rename(directory + str(old_name), directory + str(new_name))

    # for folder in folders:
    #
    #     print ("rename: " + folder)
    #
    #     file_name_list = utility.get_file_name_list(folder)
    #     for old_name in file_name_list:
    #         print ("old name: " + old_name)
    #         new_name = rename(str(old_name))
    #         print ("new name: " + new_name)
    #         rename_file(folder, old_name, new_name)
    #         print "-----------------------------------------"


folder = "./"
file_name_list = utility.get_file_name_list(folder)
for old_name in file_name_list:
    print ("old name: " + old_name)
    new_name = rename(str(old_name))
    print ("new name: " + new_name)
    rename_file(folder, old_name, new_name)
    print "-----------------------------------------"
