# coding=utf-8
import spacy
# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en_core_web_sm')
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))
stop_words.remove('not')

# Process whole documents

class FeaturExtractionSpacy:
    def __init__(self,data):
        self.data = data

    def EntityExtractionSpacy(self):
        self.data = self.data.strip(' ')
        doc = nlp(self.data)
        a = {}
        for entity in doc.ents:
            a[entity.text] =  entity.label_
        return a

    def FeatureTaggingSpacy(self):
        self.data = self.data.strip(' ')
        doc = nlp(self.data)
        a = {}
        for token in doc:
            b = []
            if token.text.lower() not in stop_words:
                b.extend([token.lemma_, token.pos_, token.tag_, token.dep_,
                    token.shape_, token.is_alpha])
                a[token.text] = b
        return a

# text = "Hey Akash, how are you?"

# print FeaturExtractionSpacy(text).EntityExtractionSpacy()


def TextSimilarity(text1,text2):
    text1 = nlp(text1)
    text2 = nlp(text2)
    similarity  = text1.similarity(text2)
    return (text1.text, text2.text,similarity)



# nlp = spacy.load('en_core_web_sm')
# doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')
#
# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#           token.shape_, token.is_alpha, token.is_stop)
# """
