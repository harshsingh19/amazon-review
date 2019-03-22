#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 20:28:30 2019

@author: harsh
"""

import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import pandas as pd
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
review =[]
rating = []
clean_rating = []
clean_review = []

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = " ".join(cleantext.split())
    return cleantext

def review_taker(soup):
    global review,clean_review;
    for i in soup.findAll("div",{"class":"a-row a-spacing-small review-data"}):
        review.append(str(i))
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


def html_data_returner(url):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        html = urllib.request.urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except :
        print("\nUnable to get the resopnse from web page.")
        pass
def review_pagefinder(soup):    
    for link in soup.findAll("a",{"class": "a-link-emphasis a-text-bold"}):
        review_link = link.get('href')
    url = "https://www.amazon.in"+review_link
    soup = html_data_returner(url)
    review_taker(soup)
    rating_taker(soup)
    return soup

def review_getter(soup):
    while len(soup.findAll("li",{ "class":"a-disabled a-last"})) == 0:
        for link in soup.findAll("li",{"class": "a-last"}):
            review_link = link.a.get('href')
        url = "https://www.amazon.in"+review_link
        soup = html_data_returner(url)
        review_taker(soup)
        rating_taker(soup)
def rating_equalizer():
    global clean_rating ,clean_review
    if len(clean_review) != len(clean_rating):
        clean_rating = clean_rating[:len(clean_review)]
def csv_saver():
    global clean_rating ,clean_review
    pairs = {'Clean_Rating': clean_rating, 'Clean_Review': clean_review}
    df = pd.DataFrame.from_dict(pairs)
    df.to_csv('Data.csv')
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
    with open("Attribute.txt","w") as f:
        f.write("Title : %s\n\nOverall Rating : %s \n\nDescription : %s"%(title,over_all_rating,description))
        f.close()
    print("Title Description and Overall Rating stored in Attribute.txt")
def word_cloud_all():
    global clean_review
    _str = ''
    for i in clean_review:
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
    plt.show()
if __name__ == "__main__":
    url = input("Enter the Product URL")
    soup = html_data_returner(url)
    if soup is not None:
        attribute_getter(soup)
        soup_review = review_pagefinder(soup)
        review_getter(soup_review)
        rating_equalizer()
        word_cloud_all()
        csv_saver()

