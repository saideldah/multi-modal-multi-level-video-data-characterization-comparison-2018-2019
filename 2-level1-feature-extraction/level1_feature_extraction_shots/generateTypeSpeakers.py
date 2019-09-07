import codecs
import xml.dom.minidom


def classify_speakers(output_xml_file, activity_threshold, extended_threshold):
    doc = xml.dom.minidom.parse(output_xml_file)
    # search the duration of the video
    duration_string = doc.getElementsByTagName("Duration")[0].childNodes[0].data
    duration = float(duration_string)
    duration_speak_total = float(doc.getElementsByTagName("DurationSpeakTotal")[0].childNodes[0].data)
    speakers = doc.getElementsByTagName("Speaker")
    if duration > 0 and duration_speak_total > 0:
        for speaker in speakers:
            performance = float(speaker.getAttribute('extent'))
            activity = duration - float(speaker.getAttribute('Inactivity'))
            activity_percentage = (activity * 100) / duration_speak_total
            extended_percentage = (performance * 100) / duration
            t1 = 0
            if activity_percentage >= activity_threshold:
                t1 = 1

            t2 = 0
            if extended_percentage >= extended_threshold:
                t2 = 1

            if performance == activity:
                speaker.setAttribute("type", "ponctuel")
            elif t1 == 1 and t2 == 0:
                speaker.setAttribute("type", "localise")
            elif t1 == 0 and t2 == 0:
                speaker.setAttribute("type", "present")
            elif t1 == 0 and t2 == 1:
                speaker.setAttribute("type", "regulier")
            elif t1 == 1 and t2 == 1:
                speaker.setAttribute("type", "important")

        file_handle = codecs.open(output_xml_file, 'wb', "utf-8")
        doc.writexml(file_handle)
        file_handle.close()

