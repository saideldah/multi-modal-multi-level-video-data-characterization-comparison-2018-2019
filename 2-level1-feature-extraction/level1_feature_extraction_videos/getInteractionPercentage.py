def intersection(start_i, end_i, start_j, end_j):
    i0 = max(start_i, start_j)
    i1 = min(end_i, end_j)
    if i0 >= i1:
        return 0
    else:
        return i1 - i0


def percentage_interaction(doc, shot_start, shot_end):
    interactions = doc.getElementsByTagName("Interaction")
    case_size = shot_end - shot_start
    percentage = {'interaction2Speakers': 0, 'interaction3Speakers': 0, 'interaction4Speakers': 0,
                  'interaction4+Speakers': 0}

    for interaction in interactions:
        interaction_start = float(interaction.getAttribute('start'))
        interaction_end = float(interaction.getAttribute('end'))

        sequence_interactions = str(interaction.childNodes[0].data).split()
        length = len(sequence_interactions)

        intersect = intersection(shot_start, shot_end, interaction_start, interaction_end)

        if length == 2:
            index = 'interaction2Speakers'
        elif length == 3:
            index = 'interaction3Speakers'
        elif length == 4:
            index = 'interaction4Speakers'
        else:
            index = 'interaction4+Speakers'
        percentage[index] = percentage[index] + intersect

    percentage['interaction2Speakers'] = round(percentage['interaction2Speakers'] * 100 / case_size, 2)
    percentage['interaction3Speakers'] = round(percentage['interaction3Speakers'] * 100 / case_size, 2)
    percentage['interaction4Speakers'] = round(percentage['interaction4Speakers'] * 100 / case_size, 2)
    percentage['interaction4+Speakers'] = round(percentage['interaction4+Speakers'] * 100 / case_size, 2)

    return percentage
