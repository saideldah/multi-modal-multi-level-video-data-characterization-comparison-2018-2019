import utility


# in this module we compute for each segment how many times there is a switch from one speaker to another speaker
# during the segment. Even if the two speakers are separated by a long gap Whenever a speaker segment ends during the
# segment and another one starts in the segment and the two speakers are different we add to the counter 1

def compute_number_speaker_switch_per_segment(doc, shot_start, shot_end):
    speaker_list = []
    speakers = doc.getElementsByTagName("SpeechSegment")
    for speaker in speakers:
        speech_id = speaker.getAttribute('spkid')
        speaker_start = float(speaker.getAttribute('stime'))
        speaker_end = float(speaker.getAttribute('etime'))
        loc = [speaker_start, speaker_end, str(speech_id)]
        if utility.is_valid_shot(speaker_start, speaker_end, shot_start, shot_end):
            speaker_list.append(loc)

    speaker_list.sort()
    if len(speaker_list) == 0:
        return 0 * 1
    case_size = shot_end - shot_start

    cmpt = 0
    for j in range(len(speaker_list) - 1):
        speaker = speaker_list[j]
        speaker_start = speaker[0]
        speaker_end = speaker[1]
        if utility.is_valid_shot(speaker_start, speaker_end, shot_start, shot_end):
            if shot_start < speaker_list[j][1] < shot_end \
                    and speaker_list[j + 1][0] < shot_end \
                    and speaker_list[j][2] != speaker_list[j + 1][2]:
                cmpt += 1
    result = cmpt * 100 / case_size
    return result
