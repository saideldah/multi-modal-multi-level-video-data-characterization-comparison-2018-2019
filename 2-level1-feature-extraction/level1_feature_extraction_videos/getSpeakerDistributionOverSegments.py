import utility


def intersection(start_i, end_i, start_j, end_j):
    i0 = max(start_i, start_j)
    i1 = min(end_i, end_j)
    if i0 >= i1:
        return 0
    else:
        return i1 - i0


def get_speaker_distribution(doc, start, end):
    speaker = doc.getElementsByTagName("Speaker")
    nb_speaker = len(speaker)
    speeches = doc.getElementsByTagName("SpeechSegment")
    mySet = set()

    for speech in speeches:
        speech_start = float(speech.getAttribute('stime'))
        speech_end = float(speech.getAttribute('etime'))
        idS = speech.getAttribute('spkid')
        # if utility.is_valid_shot(speech_start, speech_end, start, end):
        intersect = intersection(start, end, speech_start, speech_end)
        if intersect > 0:
            mySet.add(idS)

    if nb_speaker > 0:
        percentage = round(float(len(mySet)) * 100.0 / float(nb_speaker), 2)
    else:
        percentage = 0.00
    mySet.clear()
    return percentage
