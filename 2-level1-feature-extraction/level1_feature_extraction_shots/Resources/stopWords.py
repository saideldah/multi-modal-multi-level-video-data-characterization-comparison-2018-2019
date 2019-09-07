import os
import codecs
from nltk.corpus import stopwords
def words(lang):
    cwd = os.path.dirname(__file__)
    #print cwd
    try:
        stopWords = stopwords.words(lang)
        stopWords += [".", ",", "{fw}"]
        stopWords = set(stopWords)
        return stopWords
    except:
        #traceback.print_exc()
        try:
            with codecs.open(cwd + "/stopwords_" + lang + ".txt", "r", "utf8") as f:
                stopWords = f.read().lower().splitlines()
            return stopWords
        except:
            return [".", ",", "{fw}"]
    
            
if __name__ == '__main__':
    print words("")