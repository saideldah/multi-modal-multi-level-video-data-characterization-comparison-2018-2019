"""
Created on Jul 7, 2017

@author: Hasan AL Jawad
"""
import os
import sys
import traceback
from lxml import etree

from FeatureExtraction.FeaturesL1.combineLowLevelFeatures import generatePercentageDescriptors
from FeatureExtraction.Stopwords import paths

__N_ARRAY__ = 2  # Binary
__MIN_SEGMENT_DURATION__ = 300  # 5 Minutes


def generateNarrayTreeDescriptors(inputFileXML, outputFileXML, narray, split_limit):
    """
    @param inputFileXML: Level 0 xml descriptors needed to generate level 1 descriptors
    @param outputFileXML: Path to Level 1 xml descriptors file
    @param narray: Split factor that defines the structure of the tree. i.e. 2->Binarytree, 4->quadtree, 8->octree ...
    @param split_limit: Specify the minimum duration of a video or segment (in seconds), that if reached, stop splitting
    """
    if os.path.exists(inputFileXML):
        try:
            increment = 1
            leaf_level = narray
            
            generatePercentageDescriptors(inputFileXML, outputFileXML, 1)
            
            duration = float(etree.parse(inputFileXML).getroot().find("Metadata/Duration").text)
            current_segment_duration = duration/narray
            
            #if current_segment_duration < split_limit and duration >= split_limit:
            #    generatePercentageDescriptors(inputFileXML, outputFileXML, leaf_level)
            
            
            while current_segment_duration >= split_limit:
                
                generatePercentageDescriptors(inputFileXML, outputFileXML, leaf_level)
                
                increment +=1
                leaf_level = narray**(increment)
                
                current_segment_duration = current_segment_duration/narray
                
        except:
            traceback.print_exc()
            
    else:
        print "File " + inputFileXML + " doesn't exist !"
        return -1
    
    
    
    
if __name__ == '__main__':
    
    
    #logging.basicConfig(filename='/home/hassan/narrayTreeRun.log',level=logging.DEBUG)
    
    listOfVideoNames = paths.__FINAL_DESCRIPTORS_LIST_XML__
    
    '''
    @attention: This script is to run the generator on a single video file, to run it, uncomment this section and comment the rest
    nameFileVideo = "1801Media-iPhone3GWhatDoPeopleKnow259.flv.ogv"
    inputFileXML = paths.__PATH_TO_DEV_DESCRIPTORS_L0__ + nameFileVideo[:len(nameFileVideo)-8] + ".xml"
    outputFileXML = paths.__PATH_TO_DEV_DESCRIPTORS_L0__ + "6-2017\\" + nameFileVideo[:len(nameFileVideo)-8] + ".xml"
    generateNarrayTreeDescriptors(inputFileXML, outputFileXML, __N_ARRAY__, __MIN_SEGMENT_DURATION__)
    '''
    
    """
    @attention: This section is to run the script for a list of videos, provided in a file (listOfVideoNames)
    """
    if os.path.exists(listOfVideoNames):
        try:
            f = open(listOfVideoNames, 'r')
            file_names = f.read().splitlines()
            f.close()
        except IOError, e:
            print "Could not read file:", listOfVideoNames
            print str(e)
            sys.exit()
    else:
        print "File " + listOfVideoNames + " doesn't exist"
        sys.exit()
    
    
    for line in file_names:
        print line
        
        inputFileXML = paths.__PATH_TO_DEV_DESCRIPTORS_L0__ + line
        #outputFileXML = paths.__PATH_TO_DEV_DESCRIPTORS_L1__ + line
        
        #inputFileXML = "/home/hassan/6-2017/l0/"
        outputFileXML = "D:\ProjectsCode\SourceCode\PycharmProjects\VideoAnalysis\Results\\2404\\narrayTree_py\\" + line
        
        generateNarrayTreeDescriptors(inputFileXML, outputFileXML, __N_ARRAY__, __MIN_SEGMENT_DURATION__)
    