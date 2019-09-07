'''
Created on Jul 14, 2017

@author: Hasan AL Jawad
'''
import xml.dom.minidom
import FeatureExtraction.Stopwords.stopWords as stopwords

listStopWordArrays = {"eng-usa": stopwords.words('english'),
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


# def extractTextData(inputXMLFile, nbSegment):
#     # Open XML document using minidom parser
#     try:
#         DOMTreeIn = xml.dom.minidom.parse(inputXMLFile)
#     except IOError:
#         print ('Error while opening the xml file of the ASR')
#         print (inputXMLFile)
#         return -1
#
#     rootIn = DOMTreeIn.documentElement
#     TextNode = DOMTreeIn.createElement('VideoTranscript')
#
#     videoDuree = float(rootIn.getElementsByTagName("Duration")[0].firstChild.nodeValue)
#     segmentLength = round((videoDuree * 1.0) / nbSegment, 3)
#
#     SpeechSegmentList = rootIn.getElementsByTagName('SpeechSegment')
#     for segment_index in range(nbSegment):
#         currnetSegment_stime = segment_index * segmentLength
#         currentSegment_etime = currnetSegment_stime + segmentLength
#         wordList = ""
#         lang = ""
#
#         for speechSegment in SpeechSegmentList:
#             if len(speechSegment.getElementsByTagName('Word')) > 0:
#                 lang = str(speechSegment.getAttribute('lang')).strip()
#                 if lang in listStopWordArrays.keys():
#                     stopWordArray = listStopWordArrays[lang]
#                 else:
#                     stopWordArray = []
#
#                 for word in speechSegment.getElementsByTagName('Word'):
#                     word_text = word.firstChild.nodeValue.strip()
#                     #print type(word_text)
#                     if word_text not in stopWordArray:
#                         word_stime = float(word.getAttribute("stime"))
#                         word_etime = float(word.getAttribute("stime")) + float(word.getAttribute("dur"))
#
#                         if word_stime >= currnetSegment_stime and word_etime <= currentSegment_etime:
#                             wordList += word_text + ","
#
#         if len(wordList) > 1:
#             wordList = wordList[:-1]
#
#         words_element = DOMTreeIn.createElement('Words')
#         words_element.setAttribute("numSegment", str(segment_index + 1))
#         #words_element.setAttribute("lang", lang)
#         words_element.setAttribute("length", str(len(wordList.split(","))))
#         words_element.appendChild(DOMTreeIn.createTextNode(wordList))
#         TextNode.setAttribute("lang", lang)
#         TextNode.appendChild(words_element)
#
#     return TextNode


def extractTextData(inputXMLFile, timeSlots):
    try:
        DOMTreeIn = xml.dom.minidom.parse(inputXMLFile)
    except IOError:
        print ('Error while opening the xml file of the ASR')
        print (inputXMLFile)
        return -1

    rootIn = DOMTreeIn.documentElement
    TextNode = DOMTreeIn.createElement('VideoTranscript')
    listLength = len(timeSlots)
    if listLength == 1 and timeSlots[0][1] == 0:
        timeSlots[0][1] = float(rootIn.getElementsByTagName("Duration")[0].childNodes[0].data)
    SpeechSegmentList = rootIn.getElementsByTagName('SpeechSegment')
    for idx, slot in enumerate(timeSlots):
        startSeg = slot[0]
        endSeg = slot[1]
        wordList = ""
        lang = ""
        for speechSegment in SpeechSegmentList:
            if len(speechSegment.getElementsByTagName('Word')) > 0:
                lang = str(speechSegment.getAttribute('lang')).strip()
                if lang in listStopWordArrays.keys():
                    stopWordArray = listStopWordArrays[lang]
                else:
                    stopWordArray = []

                for word in speechSegment.getElementsByTagName('Word'):
                    word_text = word.firstChild.nodeValue.strip()
                    if word_text not in stopWordArray:
                        word_stime = float(word.getAttribute("stime"))
                        word_etime = float(word.getAttribute("stime")) + float(word.getAttribute("dur"))
                        if word_stime >= startSeg and word_etime <= endSeg:
                            wordList += word_text + ","
        if len(wordList) > 1:
            wordList = wordList[:-1]

        words_element = DOMTreeIn.createElement('Words')
        words_element.setAttribute("numSegment", str(len(timeSlots)))
        words_element.setAttribute("length", str(len(wordList.split(","))))
        words_element.appendChild(DOMTreeIn.createTextNode(wordList))
        TextNode.setAttribute("lang", lang)
        TextNode.appendChild(words_element)

    return TextNode
