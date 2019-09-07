import utility


def intersection(startI, endI, startJ, endJ):
    i0 = max(startI, startJ)
    i1 = min(endI, endJ)
    if i0 >= i1:
        return 0
    else:
        return i1 - i0


def percentage_speaker(doc, start, end):
    speaker_dict = dict()
    speakers = doc.getElementsByTagName("Speaker")

    for speaker in speakers:
        speaker_dict[speaker.getAttribute("spkid")] = speaker.getAttribute("type")

    speech = doc.getElementsByTagName("SpeechSegment")
    case_size = end - start
    percentage = {'ponctuel': 0, 'localise': 0, 'present': 0, 'regulier': 0, 'important': 0}

    for speaker in speech:
        speaker_start = float(speaker.getAttribute('stime'))
        speaker_end = float(speaker.getAttribute('etime'))
        idS = speaker.getAttribute('spkid')

        # if utility.is_valid_shot(speaker_start, speaker_end, start, end):
        intersect = intersection(start, end, speaker_start, speaker_end)
        speaker_type = speaker_dict[idS]
        percentage[speaker_type] = percentage[speaker_type] + intersect

    percentage['ponctuel'] = round(percentage['ponctuel'] * 100 / case_size, 2)
    percentage['localise'] = round(percentage['localise'] * 100 / case_size, 2)
    percentage['present'] = round(percentage['present'] * 100 / case_size, 2)
    percentage['regulier'] = round(percentage['regulier'] * 100 / case_size, 2)
    percentage['important'] = round(percentage['important'] * 100 / case_size, 2)
    return percentage
