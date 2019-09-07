import codecs
import xml.dom.minidom


def get_speech_sequence(input_file, threshold):
    # print input_file
    doc = xml.dom.minidom.parse(input_file)
    table_of_words = []
    speech_list = doc.getElementsByTagName("SpeechSegment")
    for speech in speech_list:
        speaker_id = speech.getAttribute('spkid')
        start = float(speech.getAttribute('stime'))
        end = float(speech.getAttribute('etime'))
        loc = [start, end, str(speaker_id)]
        table_of_words.append(loc)
    table_of_words.sort()
    if len(table_of_words) == 0:
        return []
    result = []
    list_loc = []
    i = 1
    start_index = table_of_words[0][0]
    end_index = table_of_words[0][1]
    list_loc.append(table_of_words[0][2])
    while i < len(table_of_words):
        if table_of_words[i][0] - end_index < threshold:
            end_index = table_of_words[i][1]
            list_loc.append(table_of_words[i][2])
        else:
            result.append((start_index, end_index, list_loc))
            start_index = table_of_words[i][0]
            end_index = table_of_words[i][1]
            list_loc = [table_of_words[i][2]]
        i = i + 1
    result.append((start_index, end_index, list_loc))
    return result


def write_interaction_intervention_list(output_xml_file, speech_sequence, intervention_threshold):
    length = len(speech_sequence)
    root_out = xml.dom.minidom.parse(output_xml_file)
    audio = root_out.documentElement.getElementsByTagName("Audio")[0]
    inter_ac = audio.getElementsByTagName("Interactions")
    inter_v = audio.getElementsByTagName("Interventions")
    if len(inter_ac) > 0:
        audio.removeChild(inter_ac[0])
        audio.removeChild(inter_v[0])

    interaction_list = root_out.createElement("Interactions")
    intervention_list = root_out.createElement("Interventions")
    for i in range(0, length):
        start = speech_sequence[i][0]
        end = speech_sequence[i][1]
        list_loc = speech_sequence[i][2]
        if len(list_loc) > 1:  # here means an interaction
            interaction = root_out.createElement("Interaction")
            interaction.setAttribute("start", str(start))
            interaction.setAttribute("end", str(end))
            s = str(list_loc)[1:-1]
            s = s.replace("'", "")
            s = s.replace(",", " ")
            interaction.appendChild(root_out.createTextNode(s))
            interaction_list.appendChild(interaction)
        elif len(list_loc) == 1:
            intervention = root_out.createElement("Intervention")
            if end - start > intervention_threshold:
                intervention.setAttribute("type", "long")
            else:
                intervention.setAttribute("type", "short")
            intervention.setAttribute("start", str(start))
            intervention.setAttribute("spkid", str(list_loc[0]))
            intervention.setAttribute("end", str(end))
            intervention_list.appendChild(intervention)
    audio.appendChild(interaction_list)
    audio.appendChild(intervention_list)
    try:
        output_file = codecs.open(output_xml_file, 'wb', "utf-8")
    except IOError:
        print "Unable to open file to write interactions and interventions"

    root_out.writexml(output_file)
    output_file.close()
    # print "Interactions and interventions extracted successfully"

