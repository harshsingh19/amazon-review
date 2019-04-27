#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 12:41:16 2019

@author: harsh
"""

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import os
import pandas as pd
from bs4 import BeautifulSoup
from nltk import sent_tokenize
import numpy as np
import time
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load('en')
cachedStopWords= set(STOP_WORDS)
cachedStopWords.remove('not')
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from nltk.corpus import sentiwordnet as swn
import re


def stripp(x):
    try:
        return x.strip(' ')
    except:
        return ''
def get_paras(txt):
    # txt = Preprocessing(txt).GetProcessedParas()
    doc = nlp(txt)
    sentence = [sent.string.strip() for sent in doc.sents]
    return sentence

def SentimentDecider(ss):
    Sentiment = ""
    if ss['compound'] >= 0.65 :
        Sentiment = "Strongly Positive"
    elif (ss['compound'] < 0.65 and ss['compound'] > 0.1):
        Sentiment = "Positive"
    elif ss['compound'] <= -0.65 :
        Sentiment = "Strongly Negative"
    elif (ss['compound'] > -0.65 and ss['compound'] < 0 ) :
        Sentiment = "Negative"
    else:
        Sentiment = "Neutral"
    return Sentiment


def GetSentiment(x):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(x)
    # print ss
    Sentiment = SentimentDecider(ss)
    return ss, Sentiment


def PreprocessingForVader(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in cachedStopWords]) ##stopwords
    text = re.sub("(n't|N'T)", ' not',                      text) ##Converting n't to Not
    text = re.sub("[+]\d+[.]*\d*[%]+", 'positive ',                      text) ##Converting + sign to positive
    text = re.sub("[-]\d+[.]*\d*[%]+", 'negative ',                      text) ##Converting - sign to negative
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))',' ', text ) ##URLS
    text = re.sub('<.*?>',' ',                                     text ) ##html tags
    text = re.sub(r'[\w\.-]+@[\w\.-]+',r' ',                       text ) ##email addresses
    text = re.sub('@[^\s]+',' ',                                   text ) ##Authors
    text = re.sub(r'#([^\s]+)', r'\1',                             text ) ##hash tags
    text = re.sub('\W+',' ',                                       text ) ##special char
    text = re.sub(r'^[^a-zA-Z]',r' ',                              text ) ##non words
    text = re.sub('\s*\d+\s*',' ',                                 text ) ##Numbers
    text = re.sub(r"\s+", " ",                                     text, flags=re.UNICODE)## remove multiply space and unicode
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1',                       text ) ##repetitive words
    text = re.sub(r'\s[a-z]\s', " ",                               text ) ##Single word
    return text


def SentenceNCorpusSentimentScore(Text):
    SentDF = pd.DataFrame(columns=["Comments", "Sentiment","Score"])
    CorpDF = pd.DataFrame(columns=["Corpus", "Sentiment","Score"])
    CorpDict = {}
    CorpDict['positive'] = 0
    CorpDict['negative'] = 0
    CorpDict['compound'] = 0
    CountPositive = 0
    CountNegative = 0
    for paras in get_paras(Text):
        SentList = sent_tokenize(paras)
        for Sent in SentList:
            Score, Sentiment = GetSentiment(PreprocessingForVader(Sent))
            if Sentiment in ["Positive", "Strongly Positive"]:
                CountPositive += 1
                CorpDict['positive'] += Score['pos']
            if Sentiment in ["Negative", "Strongly Negative"]:
                CountNegative += 1
                CorpDict['negative'] += Score['neg']
            if Sentiment != "Neutral":
                SentDF = SentDF.append({"Comments": (Sent),"Sentiment":  Sentiment, "Score": Score}, ignore_index=True)
                CorpDict['compound'] += Score['compound']
    if CountPositive != 0:
        CorpDict['positive'] = CorpDict['positive']/CountPositive
    if CountNegative != 0:
        CorpDict['negative'] = CorpDict['negative']/CountNegative
    if (CountPositive + CountNegative) != 0:
        CorpDict['compound'] = CorpDict['compound']/(CountPositive + CountNegative)

    CorpDF = CorpDF.append({"Corpus": (Text),"Sentiment":  SentimentDecider(CorpDict), "Score": CorpDict}, ignore_index=True)
    return SentDF, CorpDF
def SavingFile(required_df):
    FinalSentDF = pd.DataFrame(columns=["Comments", "Sentiment","Score"])
    FinalCorpDF = pd.DataFrame(columns=["Corpus", "Sentiment","Score"])
    print ("Runnig")
    for index, row in required_df.iterrows():
        SentDF, CorpDF = SentenceNCorpusSentimentScore(row['Clean_Review'])
        FinalSentDF = FinalSentDF.append(SentDF)
        FinalCorpDF = FinalCorpDF.append(CorpDF)
    print ("Saving")
    if os.path.exists("Data_Output"):
        if os.path.exists("Data_Output/SentenceSentiment.csv"):
            FinalSentDF.to_csv("Data_Output/SentenceSentiment{}.csv".format(int(time.time())),encoding='utf-8')
            FinalCorpDF.to_csv("Data_Output/CorpusSentimet{}.csv".format(int(time.time())),encoding='utf-8')
        else:
            FinalSentDF.to_csv("Data_Output/SentenceSentiment.csv",encoding='utf-8')
            FinalCorpDF.to_csv("Data_Output/CorpusSentimet.csv",encoding='utf-8')
    else:
        os.mkdir("Data_Output")
        if os.path.exists("Data_Output/SentenceSentiment.csv"):
            FinalSentDF.to_csv("Data_Output/SentenceSentiment{}.csv".format(int(time.time())),encoding='utf-8')
            FinalCorpDF.to_csv("Data_Output/CorpusSentimet{}.csv".format(int(time.time())),encoding='utf-8')
        else:
            FinalSentDF.to_csv("Data_Output/SentenceSentiment.csv",encoding='utf-8')
            FinalCorpDF.to_csv("Data_Output/CorpusSentimet.csv",encoding='utf-8')
    
   
    

def main_seniment(df):
    try:
        df = df.dropna()
        required_df = df
        required_df = required_df[required_df['Clean_Review'].apply(lambda x : stripp(x))!='']
        required_df['Clean_Review'] = required_df['Clean_Review'].apply(lambda x: BeautifulSoup(x, "lxml").text)
        required_df['paras'] = required_df['Clean_Review'].apply(lambda x: get_paras(x))
        SavingFile(required_df)   
        return 'Sucess'
    except:
        return 'Unsucess'
    
