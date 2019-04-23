#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 20:28:30 2019

@author: harsh
"""

from bs4 import BeautifulSoup
import re
import pandas as pd
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
import time
import os
import requests

review =[]
rating = []
clean_rating = []
clean_review = []
clean_timeing =[]
timeing = []
positive=[]
netural=[]
negative=[]

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = " ".join(cleantext.split())
    return cleantext

def review_taker(soup):
    global review,clean_review;
    count = 0
    for i in soup.findAll("div",{"class":"a-row a-spacing-small review-data"}):
        review.append(str(i))
        count = count +1
        print("No of reviews found on this page is", count)
    for i in review:
        clean_review.append(cleanhtml(i))
    review = []

def rating_taker(soup):
    global rating,clean_rating;  
    for i in soup.findAll("span",{ "class":"a-icon-alt"}):
        rating.append(str(i))
    rating = rating[3:13]
    for i in rating:
        clean_rating.append(cleanhtml(i))
    rating = []

def time_review(soup):
    global timeing,clean_timeing
    for i in soup.findAll("span",{ "data-hook":"review-date"}):
        timeing.append(str(i))
    for i in timeing:
        clean_timeing.append(cleanhtml(i))
    timeing=[]
def html_data_returner(url):
    headers_Get = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'}
    try:
        s = requests.Session()
        html = s.get(url, headers = headers_Get)
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup
    except :
        print("\nUnable to get the resopnse from web page.")
        pass
def review_pagefinder(soup):    
    count = 0
    for link in soup.findAll("a",{"class": "a-link-emphasis a-text-bold"}):
        review_link = link.get('href')
        count = count +1
        print("Count of no of review page ",count)
    url = "https://www.amazon.in"+review_link
    soup = html_data_returner(url)
    review_taker(soup)
    rating_taker(soup)
    time_review(soup)
    return soup

def review_getter(soup):
    count =1
    while len(soup.findAll("li",{ "class":"a-disabled a-last"})) == 0:
        for link in soup.findAll("li",{"class": "a-last"}):
            review_link = link.a.get('href')
            count = count +1
            print("Count of no of review page ",count)
        url = "https://www.amazon.in"+review_link
        time.sleep(3)
        soup = html_data_returner(url)
        review_taker(soup)
        rating_taker(soup)
        time_review(soup)
def rating_equalizer():
    global clean_rating ,clean_review,positive,negative,netural
    if len(clean_review) != len(clean_rating):
        clean_rating = clean_rating[:len(clean_review)]
def csv_saver():
    global clean_rating ,clean_review,timeing
    pairs = {'Clean_Rating': clean_rating, 'Clean_Review': clean_review, 'Time':clean_timeing}
    df = pd.DataFrame.from_dict(pairs)
    if os.path.exists("Data"):
        if os.path.exists("Data/Data.csv"):
            df.to_csv('Data/Data{}.csv'.format(int(time.time())))
        else:
            df.to_csv('Data/Data.csv')
    else:
        os.mkdir("Data")
        if os.path.exists("Data/Data.csv"):
            df.to_csv('Data/Data{}.csv'.format(int(time.time())))
        else:
            df.to_csv('Data/Data.csv')
    print("\n\n\nFile Saved as Data.csv")
def attribute_getter(soup):
    title = str(soup.findAll("div",{ "id":"titleSection"}))
    over_all_rating = str(soup.findAll("div",{ "id":"averageCustomerReviews"}))
    description = str(soup.findAll("div",{"id":"feature-bullets"}))
    hidden_description = str(soup.findAll("div",{"class":"a-expander-content a-expander-extend-content"}))
    description=description+hidden_description
    title = cleanhtml(title)
    over_all_rating = cleanhtml(over_all_rating)
    over_all_rating = over_all_rating[2:over_all_rating.index("review")+6]
    description = cleanhtml(description)
    attribute_saver(title,over_all_rating,description)
def attribute_saver(title,over_all_rating,description):
    if os.path.exists("Attribute"):
        if os.path.exists("Attribute/Attribute.txt"):
            with open('Attribute/Attribute{}.txt'.format(int(time.time())),'w') as f:
                f.write("Title : %s\n\nOverall Rating : %s \n\nDescription : %s"%(title,over_all_rating,description))
                f.close()
        else:
            with open("Attribute/Attribute.txt","w") as f:
                f.write("Title : %s\n\nOverall Rating : %s \n\nDescription : %s"%(title,over_all_rating,description))
                f.close()
    else:
        os.mkdir("Attribute")
        if os.path.exists("Attribute/Attribute.txt"):
            with open('Attribute/Attribute{}.txt'.format(int(time.time())),'w') as f:
                f.write("Title : %s\n\nOverall Rating : %s \n\nDescription : %s"%(title,over_all_rating,description))
                f.close()
        else:
            with open("Attribute/Attribute.txt","w") as f:
                f.write("Title : %s\n\nOverall Rating : %s \n\nDescription : %s"%(title,over_all_rating,description))
                f.close()
    print("Title Description and Overall Rating stored in Attribute.txt")
def word_cloud_(value):
    try:
        _str = ''
        for i in value:
            _str = _str+i
        stopwords = set(STOPWORDS)
        wc = WordCloud(width =800,
                               height = 800,
                               background_color = 'white',
                               max_words=20,
                               stopwords = stopwords,
                               min_font_size =10
                               ).generate(_str)
        plt.figure(figsize = (8,8),facecolor =None)
        plt.imshow(wc)
        plt.axis("off")
        plt.tight_layout(pad =0)
        if os.path.exists("image_data_store"):
                if os.path.exists("image_data_store/result.png"):
                    plt.savefig('image_data_store/result_{}.png'.format(int(time.time())))
                    plt.close()
                else:
                    plt.savefig('image_data_store/result.png')
                    plt.close()
        else:
                os.mkdir("image_data_store")
                if os.path.exists("image_data_store/result.png"):
                    plt.savefig('image_data_store/result_{}.png'.format(int(time.time())))
                    plt.close()
                else:
                    plt.savefig('image_data_store/result.png')
                    plt.close()
        plt.show()
    except:
        print("Unable to make word cloud")
def split_negative_positive_netural():
    try:
        global positive,netural,negative,clean_rating,clean_review
        for i in range(len(clean_rating)):
            temp = clean_rating[i]
            temp = int(float(temp[:3]))
            clean_rating[i] = temp
        _dict = dict(zip(clean_review,clean_rating))
        for i,j in _dict.items():
            if j >=4:
                positive.append(i)
            elif j<3:
                negative.append(i)
            else:
                netural.append(i)
        print("Positive Word Cloud")
        word_cloud_(positive)
        print("Negative Word Cloud")
        word_cloud_(negative)
        print("Netural Word Cloud")
        word_cloud_(netural)
        print("Overall Word Cloud")
        word_cloud_(clean_review)
        if os.path.exists("Cluster"):
            if os.path.exists('Cluster/cluster.txt'):
                with open('Cluster/cluster{}.txt'.format(int(time.time())),'w') as f:
                    f.write("Positive : %s\n\nNetural : %s \n\nNegative : %s"%(positive,netural,negative))
                    f.close()
            else:
                with open("Cluster/cluster.txt","w") as f:
                    f.write("Positive : %s\n\nNetural : %s \n\nNegative : %s"%(positive,netural,negative))
                    f.close()
        else :
            os.mkdir('Cluster')
            if os.path.exists('Cluster/cluster.txt'):
                with open('cluster{}.txt'.format(int(time.time())),'w') as f:
                    f.write("Positive : %s\n\nNetural : %s \n\nNegative : %s"%(positive,netural,negative))
                    f.close()
            else:
                with open("cluster.txt","w") as f:
                    f.write("Positive : %s\n\nNetural : %s \n\nNegative : %s"%(positive,netural,negative))
                    f.close()
        print("Made Negative Positve and Netural Cluster and saved it as cluster.txt")
    except:
        pass
if __name__ == "__main__":
    url = input("Enter the Product URL")
    soup = html_data_returner(url)
    if soup is not None:
        attribute_getter(soup)
        soup_review = review_pagefinder(soup)
        review_getter(soup_review)
        rating_equalizer()
        csv_saver()
        split_negative_positive_netural()
