import codecs
import os.path
import xml.dom.minidom
from xml.dom.minidom import Document

import numpy as np

import utility
from generateTypeSpeakers import classify_speakers
from getImageDescriptors import get_number_of_faces_variation, get_key_frames_inter_intra_segments_intensity_variation
from getInteractionPercentage import percentage_interaction
from getInteractionsInterventions import get_speech_sequence, write_interaction_intervention_list
from getInteventionPercentage import percentage_intervention
from getSpeakerDistributionOverSegments import get_speaker_distribution
from getSpeakerSwitchNumberPerSegment import compute_number_speaker_switch_per_segment
from getSpeakerTypePercentage import percentage_speaker
from getSpeechMusicPercentage import get_speech_music_non_speech_non_music_percentage
from getTextTranscripts import extract_text_data


def create_descriptors_file(output_xml_file, number_of_shots):
    # print "XML file for the descriptors does not exist yet. We will create it"
    dom_tree_out = Document()
    root = dom_tree_out.createElement("Descriptors")
    dom_tree_out.appendChild(root)
    descriptors = dom_tree_out.createElement("Shots")
    descriptors.setAttribute("count", str(number_of_shots))
    root.appendChild(descriptors)
    file_handle = codecs.open(output_xml_file, 'wb', 'utf8')
    dom_tree_out.writexml(file_handle)
    file_handle.close()
    return dom_tree_out


def generate_percentage_descriptors(input_xml_file, output_xml_file):
    number_of_shots = 1
    if number_of_shots <= 0:
        return 0
    # get the list of interaction and intervention
    speech_sequence = get_speech_sequence(input_xml_file, 2)
    write_interaction_intervention_list(input_xml_file, speech_sequence, 10)

    # classify the type of speakers
    classify_speakers(input_xml_file, 20, 20)
    if not os.path.exists(output_xml_file):
        dom_tree_out = create_descriptors_file(output_xml_file, number_of_shots)
    else:
        utility.remove_file(output_xml_file)
        dom_tree_out = create_descriptors_file(output_xml_file, number_of_shots)

    shot_number = 1
    counter = 0
    shot_descriptor_list = []
    input_dom_tree = xml.dom.minidom.parse(input_xml_file)
    category_element = input_dom_tree.getElementsByTagName("Category")
    # print category_element
    category = category_element[0].firstChild.nodeValue

    duration_element = input_dom_tree.getElementsByTagName("Duration")
    # print duration_element
    video_duration = duration_element[0].firstChild.nodeValue

    shot_item = {"start": 0, "end": float(video_duration), "duration": float(video_duration)}
    start = shot_item["start"]
    end = shot_item["end"]
    duration = shot_item["duration"]

    shot_descriptors = dom_tree_out.createElement("Shot")
    shot_descriptors.setAttribute("start", str(start))
    shot_descriptors.setAttribute("end", str(end))
    shot_descriptors.setAttribute("duration", str(duration))
    # print duration
    shot_descriptors.setAttribute("duration_percentage", str((duration * 100) / 11367))
    shot_descriptors.setAttribute("shot_number", str(shot_number))
    shot_descriptors.setAttribute("category", category)

    shot_number += 1
    counter += 1
    if end - start > 0:
        # region Interaction (get interaction percentage then add the values in the xml file)
        # print "get interaction percentage then add the values in the xml file:"
        # print 'start:  {}'.format(datetime.datetime.now().time())
        p_interaction = percentage_interaction(input_dom_tree, start, end)

        interaction_list = dom_tree_out.createElement("Interactions")
        inter2sp = dom_tree_out.createElement("Interaction")
        inter2sp.setAttribute("numberSpeakers", "2")
        inter2sp.appendChild(dom_tree_out.createTextNode(str(p_interaction["interaction2Speakers"])))
        interaction_list.appendChild(inter2sp)

        inter3sp = dom_tree_out.createElement("Interaction")
        inter3sp.setAttribute("numberSpeakers", "3")
        inter3sp.appendChild(dom_tree_out.createTextNode(str(p_interaction["interaction3Speakers"])))
        interaction_list.appendChild(inter3sp)

        inter4sp = dom_tree_out.createElement("Interaction")
        inter4sp.setAttribute("numberSpeakers", "4")
        inter4sp.appendChild(dom_tree_out.createTextNode(str(p_interaction["interaction4Speakers"])))
        interaction_list.appendChild(inter4sp)

        inter5sp = dom_tree_out.createElement("Interaction")
        inter5sp.setAttribute("numberSpeakers", "4+")
        inter5sp.appendChild(dom_tree_out.createTextNode(str(p_interaction["interaction4+Speakers"])))
        interaction_list.appendChild(inter5sp)
        shot_descriptors.appendChild(interaction_list)
        # print 'end:  {}'.format(datetime.datetime.now().time())
        # endregion

        # region Intervention (get intervention percentage and add them to the file)
        # print "get intervention percentage and add them to the file:"
        # print 'start:  {}'.format(datetime.datetime.now().time())
        p_intervention = percentage_intervention(input_dom_tree, start, end)
        intervention_list = dom_tree_out.createElement("Interventions")
        inter_short = dom_tree_out.createElement("Intervention")
        inter_short.setAttribute("type", "short")
        inter_short.appendChild(dom_tree_out.createTextNode(str(p_intervention["short"])))
        inter_long = dom_tree_out.createElement("Intervention")
        inter_long.setAttribute("type", "long")
        inter_long.appendChild(dom_tree_out.createTextNode(str(p_intervention["long"])))
        intervention_list.appendChild(inter_short)
        intervention_list.appendChild(inter_long)
        shot_descriptors.appendChild(intervention_list)
        # print 'end:  {}'.format(datetime.datetime.now().time())
        # endregion

        # region SpeakersTypeList (get speaker distribution and add the values to the xml)
        # print "get speaker distribution and add the values to the xml:"
        # print 'start:  {}'.format(datetime.datetime.now().time())
        p_speakers = percentage_speaker(input_dom_tree, start, end)
        speaker_type_list = dom_tree_out.createElement("SpeakersTypeList")
        sp_type = dom_tree_out.createElement("SpeakersType")

        punctual = dom_tree_out.createElement("Ponctuel")
        punctual.appendChild(dom_tree_out.createTextNode(str(p_speakers["ponctuel"])))
        sp_type.appendChild(punctual)

        localise = dom_tree_out.createElement("Localise")
        localise.appendChild(dom_tree_out.createTextNode(str(p_speakers["localise"])))
        sp_type.appendChild(localise)

        present = dom_tree_out.createElement("Present")
        present.appendChild(dom_tree_out.createTextNode(str(p_speakers["present"])))
        sp_type.appendChild(present)

        regular = dom_tree_out.createElement("Regulier")
        regular.appendChild(dom_tree_out.createTextNode(str(p_speakers["regulier"])))
        sp_type.appendChild(regular)

        important = dom_tree_out.createElement("Important")
        important.appendChild(dom_tree_out.createTextNode(str(p_speakers["important"])))
        sp_type.appendChild(important)

        speaker_type_list.appendChild(sp_type)
        shot_descriptors.appendChild(speaker_type_list)
        # print 'end:  {}'.format(datetime.datetime.now().time())
        # endregion

        # region SpeakersDistribution (get speaker distribution over segments (how many speakers from the total
        # number is speaking during the segment)
        # print "get speaker distribution over segments (how many speakers from the total " \
        #       "number is speaking during the segment:"
        # print 'start:  {}'.format(datetime.datetime.now().time())
        d_speakers = get_speaker_distribution(input_dom_tree, start, end)
        d_speakers_list = dom_tree_out.createElement("SpeakersDistribution")
        d_speaker = dom_tree_out.createElement("SpeakerDistribution")
        d_speaker.appendChild(dom_tree_out.createTextNode(str(d_speakers)))
        d_speakers_list.appendChild(d_speaker)
        shot_descriptors.appendChild(d_speakers_list)
        # print 'end:  {}'.format(datetime.datetime.now().time())
        # endregion

        # region nbFacesList (get the list of nb of faces during segments)
        # print "get the list of nb of faces during segments "
        # print 'start:  {}'.format(datetime.datetime.now().time())
        nb_faces_result = get_number_of_faces_variation(input_dom_tree, start, end)
        nb_faces_list = dom_tree_out.createElement("nbFacesList")
        nb_faces = dom_tree_out.createElement("nbFaces")
        ls = list(nb_faces_result)
        mean = 0
        sigma = 0
        if len(ls) != 0:
            mean = np.mean(ls)
            sigma = np.std(ls)

        min_node = dom_tree_out.createElement("MeanNbFaces")
        min_node.appendChild(dom_tree_out.createTextNode(str(mean)))
        nb_faces.appendChild(min_node)
        max_node = dom_tree_out.createElement("StdNbFaces")
        max_node.appendChild(dom_tree_out.createTextNode(str(sigma)))
        nb_faces.appendChild(max_node)
        nb_faces_list.appendChild(nb_faces)
        shot_descriptors.appendChild(nb_faces_list)
        # print 'end:  {}'.format(datetime.datetime.now().time())
        # endregion

        # region IntensityVariation (get the list of intensity variations)
        # print "get the list of intensity variations "
        # print 'start:  {}'.format(datetime.datetime.now().time())
        list_intensity_variations_inter, \
        list_intensity_variations_intra, \
        nb_transitions = get_key_frames_inter_intra_segments_intensity_variation(input_dom_tree, start, end)

        intensity_var = dom_tree_out.createElement("IntensityVariation")
        shot_descriptors.appendChild(intensity_var)

        inter_intensity_variation_list = dom_tree_out.createElement("InterIntensityVariationList")

        for intensity_variations_inter in list_intensity_variations_inter:
            i_variation = dom_tree_out.createElement("InterIntensityVariation")
            normalized_intensity_variations_inter = (intensity_variations_inter * 100) / 255
            txt_node = dom_tree_out.createTextNode(str(normalized_intensity_variations_inter))
            i_variation.appendChild(txt_node)
            inter_intensity_variation_list.appendChild(i_variation)
        intensity_var.appendChild(inter_intensity_variation_list)

        intra_intensity_variation_list = dom_tree_out.createElement("IntraIntensityVariationList")

        for intra_intensity_variation in list_intensity_variations_intra:
            i_variation = dom_tree_out.createElement("IntraIntensityVariation")
            normalized_intra_intensity_variation = (intra_intensity_variation * 100) / 255
            txt_node = dom_tree_out.createTextNode(str(normalized_intra_intensity_variation))
            i_variation.appendChild(txt_node)
            intra_intensity_variation_list.appendChild(i_variation)
        intensity_var.appendChild(intra_intensity_variation_list)

        nb_shot_transitions_list = dom_tree_out.createElement("NumberShotTransitionList")
        nb_trans = dom_tree_out.createElement("NumberShotTransition")
        txt_node = dom_tree_out.createTextNode(str(nb_transitions * 100))
        nb_trans.appendChild(txt_node)
        nb_shot_transitions_list.appendChild(nb_trans)
        shot_descriptors.appendChild(nb_shot_transitions_list)
        # print 'end:  {}'.format(datetime.datetime.now().time())
        # endregion

        # region Number Speaker Transition List
        # print "Number Speaker Transition List "
        # print 'start:  {}'.format(datetime.datetime.now().time())
        nb_speaker_transition = compute_number_speaker_switch_per_segment(input_dom_tree, start, end)
        nb_speaker_transition_list = dom_tree_out.createElement("NumberSpeakerTransitionList")

        nb_trans = dom_tree_out.createElement("NumberSpeakerTransition")
        txt_node = dom_tree_out.createTextNode(str(nb_speaker_transition))
        nb_trans.appendChild(txt_node)
        nb_speaker_transition_list.appendChild(nb_trans)

        shot_descriptors.appendChild(nb_speaker_transition_list)
        # print 'end:  {}'.format(datetime.datetime.now().time())
        # endregion

        # region Speech Music Alignment List
        # print "Speech Music Alignment List "
        # print 'start:  {}'.format(datetime.datetime.now().time())
        list_speech_music_combinations = get_speech_music_non_speech_non_music_percentage(input_dom_tree, start, end)
        s_m_ns_nm_list = dom_tree_out.createElement("SpeechMusicAlignmentList")

        alignment = dom_tree_out.createElement("SpeechMusicAlignment")

        s = dom_tree_out.createElement("Speech")
        s.appendChild(dom_tree_out.createTextNode(str(round(list_speech_music_combinations["P"], 2))))
        alignment.appendChild(s)

        m = dom_tree_out.createElement("Music")
        m.appendChild(dom_tree_out.createTextNode(str(round(list_speech_music_combinations["M"], 2))))
        alignment.appendChild(m)

        s_m = dom_tree_out.createElement("SpeechWithMusic")
        s_m.appendChild(dom_tree_out.createTextNode(str(round(list_speech_music_combinations["PM"], 2))))
        alignment.appendChild(s_m)

        s_nm = dom_tree_out.createElement("SpeechWithNonMusic")
        s_nm.appendChild(dom_tree_out.createTextNode(str(round(list_speech_music_combinations["PNM"], 2))))
        alignment.appendChild(s_nm)

        ns_m = dom_tree_out.createElement("NonSpeechWithMusic")
        ns_m.appendChild(dom_tree_out.createTextNode(str(round(list_speech_music_combinations["NPM"], 2))))
        alignment.appendChild(ns_m)

        ns_nm = dom_tree_out.createElement("NonSpeechWithNonMusic")
        ns_nm.appendChild(dom_tree_out.createTextNode(str(round(list_speech_music_combinations["NPNM"], 2))))
        alignment.appendChild(ns_nm)

        s_m_ns_nm_list.appendChild(alignment)
        shot_descriptors.appendChild(s_m_ns_nm_list)
        # print 'end:  {}'.format(datetime.datetime.now().time())
        # endregion

        # region get the list of words
        # print "get the list of words "
        # print 'start:  {}'.format(datetime.datetime.now().time())
        data = extract_text_data(input_dom_tree, start, end)
        shot_descriptors.appendChild(data)
        # print 'end:  {}'.format(datetime.datetime.now().time())
        # endregion
        shot_descriptor_list.append(shot_descriptors)
        # print "*************************************************************"
        if counter > 5:
            counter = 0
            dom_tree_out = xml.dom.minidom.parse(output_xml_file)
            for sh in shot_descriptor_list:
                dom_tree_out.getElementsByTagName("Shots")[0].appendChild(sh)
            file_handle = codecs.open(output_xml_file, 'wb', 'utf8')
            dom_tree_out.writexml(file_handle)
            file_handle.close()
            shot_descriptor_list = []
            dom_tree_out = Document()

    dom_tree_out = xml.dom.minidom.parse(output_xml_file)
    for sh in shot_descriptor_list:
        dom_tree_out.getElementsByTagName("Shots")[0].appendChild(sh)
    file_handle = codecs.open(output_xml_file, 'wb', 'utf8')
    dom_tree_out.writexml(file_handle)
    file_handle.close()
    # print "Combination of descriptors are generated successfully for file:" + input_xml_file
