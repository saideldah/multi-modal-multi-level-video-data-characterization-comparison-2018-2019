def intersection(start_i, end_i, start_j, end_j):
    i0 = max(start_i, start_j)
    i1 = min(end_i, end_j)
    if i0 >= i1:
        return 0
    else:
        return i1 - i0


def percentage_intervention(doc, shot_start, shot_end):
    interventions = doc.getElementsByTagName("Intervention")
    case_size = shot_end - shot_start
    percentage = {'long': 0, 'short': 0}

    for intervention in interventions:
        intervention_start = float(intervention.getAttribute('start'))
        intervention_end = float(intervention.getAttribute('end'))
        intervention_type = intervention.getAttribute('type')
        intersect = intersection(shot_start, shot_end, intervention_start, intervention_end)
        percentage[intervention_type] = percentage[intervention_type] + intersect
        # print "intervention_start: " + str(intervention_start)
        # print "intervention_end: " + str(intervention_end)
        # print "shot_start: " + str(shot_start)
        # print "shot_end: " + str(shot_end)
        # print "shot_end: " + str(percentage[intervention_type])

    percentage['long'] = round(percentage['long'] * 100 / case_size, 2)
    percentage['short'] = round(percentage['short'] * 100 / case_size, 2)
    return percentage
