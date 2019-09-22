import math

import utility


def intersection(start_i, end_i, start_j, end_j):
    i0 = max(start_i, start_j)
    i1 = min(end_i, end_j)
    if i0 >= i1:
        return 0
    else:
        return i1 - i0


def get_number_of_faces_variation(doc, start, end):
    shot_list = doc.getElementsByTagName("Shot")
    faces_list = set()
    for shot in shot_list:
        nbFaces = int(shot.getAttribute('nbFaces'))
        percentage_faces = float(shot.getAttribute('percentageFaces'))
        shot_start = float(shot.getAttribute('stime'))
        shot_end = float(shot.getAttribute('etime'))
        # if utility.is_valid_shot(shot_start, shot_end, start, end):
        intersect = intersection(start, end, shot_start, shot_end)
        if intersect > 0:
            faces_list.add(float(nbFaces * percentage_faces))

    percentage = faces_list
    return percentage


def get_mean_variance_patches(all_patches_segment):
    sum_patches = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    variance_patches = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    patch = []

    for i in range(len(all_patches_segment)):
        patch = all_patches_segment[i]
        sum_patches = [sum_patches[j] + patch[j] for j in range(len(patch))]
    mean_patches = []
    for j in range(len(sum_patches)):
        if len(all_patches_segment) > 0:
            mean_patches.append(round(sum_patches[j] / len(all_patches_segment)))
        else:
            mean_patches.append(0.0)

    for i in range(len(all_patches_segment)):
        patch = all_patches_segment[i]
        for j in range(len(patch)):
            variance_patches[j] = variance_patches[j] + ((patch[j] - mean_patches[j]) * (patch[j] - mean_patches[j]))
    for i in range(len(patch)):
        variance_patches[i] = round(math.sqrt(variance_patches[i] / len(all_patches_segment)))
    return mean_patches, variance_patches


def get_key_frames_inter_intra_segments_intensity_variation(doc, start, end):
    # in this method we calculate the inter and intra segment variation of the intensity colors over the patches
    # we compute also the number of transitions from one complete_video to another complete_video inside a segment
    shot_list = doc.getElementsByTagName("Shot")

    duration = float(doc.getElementsByTagName("Duration")[0].childNodes[0].data)
    variation_inter = []
    variation_intra = []
    patches_list = []
    nb_transitions = []

    averagePatches = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    all_patches_segment = []
    cmpt = 0
    for shot in shot_list:
        patches = [int(v) for v in shot.getAttribute('Patches')[1:-1].split(",")]
        shot_start = float(shot.getAttribute('stime'))
        shot_end = float(shot.getAttribute('etime'))
        # if utility.is_valid_shot(shot_start, shot_end, start, end):
        intersect = intersection(start, end, shot_start, shot_end)
        if intersect > 0:
            weight = float(intersect) / (end - start)
            averagePatches = [averagePatches[j] + weight * patches[j] for j in range(len(patches))]
            all_patches_segment.append(patches)
        if start < shot_end < end:
            cmpt = cmpt + 1

    mean_patches, variance_patches = get_mean_variance_patches(all_patches_segment)
    if duration > 0:
        nb_transitions = cmpt * 100 / duration
    else:
        nb_transitions = 0
    variation_intra = variance_patches
    patches_list.append(averagePatches)

    variation_inter_element = [round(abs(patches_list[0][j]), 2) for j in range(0, len(patches_list[0]))]
    variation_inter = variation_inter_element

    return variation_inter, variation_intra, nb_transitions
