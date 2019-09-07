import xml.dom.minidom

import Resources.stopWords as stopwords

list_stop_word_arrays = {"eng-usa": stopwords.words('english'),
                         "spa": stopwords.words('spanish'),
                         "fre": stopwords.words('french'),
                         "slo": stopwords.words('slovak'),
                         "kor": stopwords.words('korean'),
                         "cze": stopwords.words('czech'),
                         "tur": stopwords.words('turkish'),
                         "por": stopwords.words('portuguese'),
                         "dut": stopwords.words('dutch'),
                         "fas": stopwords.words('fas'),
                         "swe": stopwords.words('swedish'),
                         "hun": stopwords.words('hungarian'),
                         "nor": stopwords.words('norwegian'),
                         "rus": stopwords.words('russian'), }


def extract_text_data(DOMTreeIn, start, end):
    root_in = DOMTreeIn.documentElement
    text_node = DOMTreeIn.createElement('VideoTranscript')

    speech_segment_list = root_in.getElementsByTagName('SpeechSegment')

    current_segment_start_time = start
    current_segment_end_time = end
    word_list = ""
    lang = ""

    for speech_segment in speech_segment_list:
        if len(speech_segment.getElementsByTagName('Word')) > 0:
            lang = str(speech_segment.getAttribute('lang')).strip()
            if lang in list_stop_word_arrays.keys():
                stop_word_array = list_stop_word_arrays[lang]
            else:
                stop_word_array = []

            for word in speech_segment.getElementsByTagName('Word'):
                word_text = word.firstChild.nodeValue.strip()
                # print type(word_text)
                if word_text not in stop_word_array:
                    word_start_time = float(word.getAttribute("stime"))
                    word_etime = float(word.getAttribute("stime")) + float(word.getAttribute("dur"))

                    if word_start_time >= current_segment_start_time and word_etime <= current_segment_end_time:
                        word_list += word_text + ","

    if len(word_list) > 1:
        word_list = word_list[:-1]
    length = len(word_list.split(","))
    max_number_of_words = 7640
    words_element = DOMTreeIn.createElement('Words')
    words_element.setAttribute("length", str(length))
    words_element.setAttribute("length_percentage", str(float(length * 100) / max_number_of_words))
    words_element.appendChild(DOMTreeIn.createTextNode(word_list))
    text_node.setAttribute("lang", lang)
    text_node.appendChild(words_element)

    return text_node
