import xml.dom.minidom
import utility


def return_by_tag(doc, tag_name):
    tab = doc.getElementsByTagName(tag_name)
    Tab = []
    for s in tab:
        start = float(s.getAttribute('start'))
        end = float(s.getAttribute('end'))
        loc = [start, end]
        Tab.append(loc)
    Tab.sort()
    return Tab


def intersection(startI, endI, startJ, endJ):
    i0 = max(startI, startJ)
    i1 = min(endI, endJ)
    return i0, i1


def intersection_with_segment(shot_start, shot_end, Tab1, Tab2):
    Intersection = 0
    for j in range(len(Tab1)):
        for k in range(len(Tab2)):
            tab1_start = Tab1[j][0]
            tab2_start = Tab2[k][0]
            tab1_end = Tab1[j][1]
            tab2_end = Tab2[k][1]
            if tab1_end < tab2_start:
                break
            i0, i1 = intersection(tab1_start, tab1_end, tab2_start, tab2_end)
            if i0 < i1:
                dI, fI = intersection(shot_start, shot_end, i0, i1)
                if dI < fI:
                    Intersection = Intersection + (fI - dI)
    return Intersection


def intersection_segment_segment(shot_start, shot_end, tab):
    Intersection = 0

    for k in range(len(tab)):
        start = tab[k][0]
        end = tab[k][1]
        if utility.is_valid_shot(start, end, shot_start, shot_end):
            dI, fI = intersection(shot_start, shot_end, start, end)
            if dI < fI:
                Intersection = Intersection + (fI - dI)
    return Intersection


def get_speech_music_non_speech_non_music_percentage(input_dom_tree, shot_start, shot_end):
    video = {'P': 0, 'M': 0, 'PM': 0, 'NPM': 0, 'PNM': 0, 'NPNM': 0}

    parol_tab = return_by_tag(input_dom_tree, 'Speech')
    music_tab = return_by_tag(input_dom_tree, 'Music')
    non_parol_tab = return_by_tag(input_dom_tree, 'NonSpeech')
    non_music_tab = return_by_tag(input_dom_tree, 'NonMusic')
    case_size = shot_end - shot_start

    video['P'] = video['P'] + intersection_segment_segment(shot_start, shot_end, parol_tab) * 100.0 / case_size
    video['M'] = video['M'] + intersection_segment_segment(shot_start, shot_end, music_tab) * 100.0 / case_size
    video['PM'] = video['PM'] + intersection_with_segment(shot_start, shot_end, parol_tab,
                                                          music_tab) * 100.0 / case_size
    video['NPM'] = video['NPM'] + intersection_with_segment(shot_start, shot_end, non_parol_tab,
                                                            music_tab) * 100.0 / case_size
    video['PNM'] = video['PNM'] + intersection_with_segment(shot_start, shot_end, parol_tab,
                                                            non_music_tab) * 100.0 / case_size
    video['NPNM'] = video['NPNM'] + intersection_with_segment(shot_start, shot_end, non_parol_tab,
                                                              non_music_tab) * 100.0 / case_size

    return video
