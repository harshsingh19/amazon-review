import matplotlib.pyplot as plt
import time
import os
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import gc
import logging 

class Amazon():
    def __init__(self):
        super().__init__()
        self.headers_Get = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'}
        self.setupLogging()
        self.clean_rating = []
        self.clean_review_title =[]
        self.clean_review = []
        self.clean_review_name = []
        self.clean_timeing =[]
        self.product_link =[]
        self.search_links =[]
        self.title=""
        self.kinddleInclude = False
        
    def setupLogging(self):
        self.logger =logging.getLogger("Harsh")
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        if os.path.exists("Logs"):
            if os.path.exists('Logs/AmazonLog.log'):
                fh = logging.FileHandler('Logs/AmazonLog{}.log'.format(int(time.time())))
            else:
                 fh = logging.FileHandler('Logs/AmazonLog.log')
        else :
            os.mkdir('Logs')
            if os.path.exists('Logs/AmazonLog.log'):
                fh = logging.FileHandler('Logs/AmazonLog{}.log'.format(int(time.time())))
            else:
                fh = logging.FileHandler('Logs/AmazonLog.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ih = logging.StreamHandler()
        ih.setLevel(logging.INFO)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        ih.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.addHandler(ih)



    def html_data_returner(self,url):
        try:
            s = requests.Session()
            html = s.get(url,headers = self.headers_Get)
            soup = BeautifulSoup(html.text, 'html.parser')
            return soup
        except :
            self.logger.error("Exception occurred", exc_info=True)
            pass
    def cleanhtml(self,raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext = " ".join(cleantext.split())
        return cleantext
    def rating_equalizer(self):
        if len(self.clean_review) != len(self.clean_rating):
            self.clean_rating = self.clean_rating[:len(self.clean_review)]
            self.clean_review_name = self.clean_review_name[:len(self.clean_review)]
    def product_pagefinder(self,soup):    
        try:
            soup = BeautifulSoup(str(soup).strip('<!-- EndNav -->'),'html.parser')
            for i in soup.findAll("span",{ "class":"aok-inline-block zg-item"}):
                for link in i.findAll("a",{"class": "a-link-normal"}):
                    if "product-reviews" not in link.get('href'):
                        self.product_link.append("https://www.amazon.in"+link.get('href'))
        except:
            self.logger.error("Exception occurred", exc_info=True)
            pass
    def product_nextPagefinder(self,url):
        try:
            soup = self.html_data_returner(url)
            if soup is not None:
                
                self.product_pagefinder(soup)
                while len(soup.findAll("li",{ "class":"a-disabled a-last"})) == 0:
                    for link in soup.findAll("li",{"class": "a-last"}):
                        review_link = link.a.get('href')
                    url = "https://www.amazon.in"+review_link
                    soup = self.html_data_returner(url)
                    self.product_pagefinder(soup)
        except:
            self.logger.error("Exception occurred", exc_info=True)
            pass
    def search_pagefinder(self,soup):
        try:
            for link in soup.findAll("h2",{"class":"a-size-mini a-spacing-none a-color-base s-line-clamp-2"}):
                for i in link.findAll("a",{"class": "a-link-normal a-text-normal"}):
                    searchLinks = i.get('href')
                    if "/gp/video/" not in searchLinks:
                        self.search_links.append("https://www.amazon.in"+searchLinks)
        except :
            self.logger.error("Exception occurred", exc_info=True)
            pass
    def search_nextPagefinder(self,url):
        try:
            soup = self.html_data_returner(url)
            if soup is not None:
                self.search_pagefinder(soup)
                while len(soup.findAll("li",{ "class":"a-disabled a-last"})) == 0:
                    for link in soup.findAll("li",{"class": "a-last"}):
                        review_link = link.a.get('href')
                    url = "https://www.amazon.in"+review_link
                    soup = self.html_data_returner(url)
                    self.search_pagefinder(soup)
        except:
            self.logger.error("Exception occurred", exc_info=True)
            pass
    def review_pageFinder(self,review_link):
        url = "https://www.amazon.in"+review_link
        soup = self.html_data_returner(url)
        self.review_taker(soup)
        self.rating_taker(soup)
        self.time_review(soup)
        self.review_name_taker(soup)
        self.review_title_taker(soup)
        return url
    def review_productPage(self,url):    
        try:
            soup = self.html_data_returner(url)
            if soup is not None:
                for link in soup.findAll("a",{"class": "a-link-emphasis a-text-bold"}):
                    review_link = link.get('href')
                #if this is kinddle page and and kinddel is excluded
                if len(soup.findAll("div",{"id":"MediaMatrix","class":"feature","data-feature-name":"MediaMatrix", "data-cel-widget":"MediaMatrix"})) != 0 and self.kinddleInclude == False:
                    return "Kinndle Excluded"
                else:
                    return self.review_pageFinder(review_link)
        except:
            self.logger.error("Exception occurred", exc_info=True)
            pass
    def review_getter(self,url):
        try:
            count =0
            soup = self.html_data_returner(url)
            if soup is not None:
                while len(soup.findAll("li",{ "class":"a-disabled a-last"})) == 0:
                    for link in soup.findAll("li",{"class": "a-last"}):
                        review_link = link.a.get('href')
                        count = count +1
                        self.logger.info("Count of no of review page "+str(count))
                    url = "https://www.amazon.in"+review_link
                    time.sleep(3)
                    soup = self.html_data_returner(url)
                    self.review_taker(soup)
                    self.rating_taker(soup)
                    self.time_review(soup)
                    self.review_name_taker(soup)
                    self.review_title_taker(soup)
        except:
            self.logger.error("Exception occurred", exc_info=True)
            pass  
    def review_taker(self,soup):
        review =[]
        count = 0
        for i in soup.findAll("div",{"class":"a-row a-spacing-small review-data"}):
            review.append(str(i))
            count = count +1
            self.logger.info("No of reviews found on this page is "+str(count))
        for i in review:
            self.clean_review.append(self.cleanhtml(i))
        review = []

    def review_name_taker(self,soup):
        review_name = []
        for i in soup.findAll("div",{"class":"a-profile-content"}):
            review_name.append(str(i))
        if len(soup.findAll("div",{"class":"a-row view-point"})) != 0:
            review_name = review_name[2:]
        for i in review_name:
            self.clean_review_name.append(self.cleanhtml(i))
        review_name = []
    def review_title_taker(self,soup):
        review_title = []
        for i in soup.findAll("a",{"data-hook":"review-title"}):
            review_title.append(str(i))
        for i in review_title:
            self.clean_review_title.append(self.cleanhtml(i))
        review_title = []
    def rating_taker(self,soup):
        rating  = []
        for i in soup.findAll("span",{ "class":"a-icon-alt"}):
            rating.append(str(i))
        rating = rating[3:13]
        for i in rating:
            self.clean_rating.append(self.cleanhtml(i))
        rating = []

    def time_review(self,soup):
        timeing = []
        for i in soup.findAll("span",{ "data-hook":"review-date"}):
            timeing.append(str(i))
        for i in timeing:
            self.clean_timeing.append(self.cleanhtml(i))
        timeing=[]
        
    def attribute_getter(self,url):
        soup = self.html_data_returner(url)
        if soup is not None:
            self.title = str(soup.findAll("div",{ "id":"titleSection"}))
            self.over_all_rating = str(soup.findAll("div",{ "id":"averageCustomerReviews"}))
            self.description = str(soup.findAll("div",{"id":"feature-bullets"}))
            self.hidden_description = str(soup.findAll("div",{"class":"a-expander-content a-expander-extend-content"}))
            self.description=self.description+self.hidden_description
            self.title = self.cleanhtml(self.title)
            self.over_all_rating = self.cleanhtml(self.over_all_rating)
            self.over_all_rating = self.over_all_rating[2:32]
            self.description = self.cleanhtml(self.description)
            self.attribute_saver()
        else:
            self.logger.warning("Soup value is empty in attribute_getter", exc_info=True)
    def attribute_saver(self):
        try:
            pairs = {'Title': self.title, 'Over_All_Rating': self.over_all_rating, 'Description':self.description}
            df = pd.Series(pairs)
            df = pd.DataFrame.from_dict(df)
            df = df.transpose()
            if os.path.exists("Attribute"):
                if os.path.exists("Attribute/Attribute.txt"):
                    with open('Attribute/Attribute{}.txt'.format(int(time.time())),'w') as f:
                        f.write("Title : %s\n\nOverall Rating : %s \n\nDescription : %s"%(self.title,self.over_all_rating,self.description))
                        f.close()
                else:
                    with open("Attribute/Attribute.txt","w") as f:
                        f.write("Title : %s\n\nOverall Rating : %s \n\nDescription : %s"%(self.title,self.over_all_rating,self.description))
                        f.close()
            else:
                os.mkdir("Attribute")
                if os.path.exists("Attribute/Attribute.txt"):
                    with open('Attribute/Attribute{}.txt'.format(int(time.time())),'w') as f:
                        f.write("Title : %s\n\nOverall Rating : %s \n\nDescription : %s"%(self.title,self.over_all_rating,self.description))
                        f.close()
                else:
                    with open("Attribute/Attribute.txt","w") as f:
                        f.write("Title : %s\n\nOverall Rating : %s \n\nDescription : %s"%(self.title,self.over_all_rating,self.description))
                        f.close()
                        
            if os.path.exists("Attribute"):
                if os.path.exists('Attribute/Attribute.csv'):
                    df.to_csv('Attribute/Attribute{}.csv'.format(int(time.time())))
                else:
                    df.to_csv('Attribute/Attribute.csv')
            else :
                os.mkdir('Attribute')
                if os.path.exists('Attribute/Attribute.csv'):
                    df.to_csv('Attribute/Attribute{}.csv'.format(int(time.time())))
                else:
                    df.to_csv('Attribute/Attribute.csv')
            self.logger.info("Title Description and Overall Rating stored in Attribute.csv")
        except :
            self.logger.error("Exception occurred", exc_info=True)
            pass
    def csv_saver(self):
        pairs = {'Reviewer Name':self.clean_review_name,'Clean_Rating': self.clean_rating, 'Clean_Review': self.clean_review, 'Time':self.clean_timeing, "Review title":self.clean_review_title}
        self.logger.info("Count of reviewer Name :"+str(len(self.clean_review_name)))
        self.logger.info("Count of reviewer raiting :"+str(len(self.clean_rating)))
        self.logger.info("Count of reviewer review :"+str(len(self.clean_review)))
        self.logger.info("Count of reviewer time :"+str(len(self.clean_timeing)))
        self.logger.info("Count of reviewer title :"+str(len(self.clean_review_title)))
        self.df = pd.DataFrame.from_dict(pairs)
        if os.path.exists("Data"):
            if os.path.exists("Data/Data.csv"):
                self.df.to_csv('Data/Data{}.csv'.format(int(time.time())))
            else:
                self.df.to_csv('Data/Data.csv')
        else:
            os.mkdir("Data")
            if os.path.exists("Data/Data.csv"):
                self.df.to_csv('Data/Data{}.csv'.format(int(time.time())))
            else:
                self.df.to_csv('Data/Data.csv')
        self.logger.info("\n\n\nFile Saved as Data.csv")
        self.clean_rating = []
        self.clean_review = []
        self.clean_timeing = []
        self.clean_review_name = []
        self.clean_review_title =[]
        self.title = ""
        return self.df
    def product_URL(self,url):
        self.logger.info("Product Garbage collector: collected %d objects.(START)" % (gc.collect()))
        if url is not None:
            self.attribute_getter(url)
            self.logger.info("Titel of URL = "+self.title)
            link_review = self.review_productPage(url)
            self.review_getter(link_review)
            self.rating_equalizer()
            self.csv_saver()
        else:
            self.logger.info("Please enter Valid URL")
        self.logger.info("Product Garbage collector: collected %d objects.(END)" % (gc.collect()))

    def bestSeller_URL(self,url):
        self.logger.info("BestSeller Garbage collector: collected %d objects.(START)" % (gc.collect()))
        if url is not None:
            self.product_nextPagefinder(url)
            if self.product_link is not None:
                for link in self.product_link:
                    self.attribute_getter(link)
                    self.logger.info("Titel of URL = "+self.title)
                    link_review = self.review_productPage(link)
                    self.review_getter(link_review)
                    self.rating_equalizer()
                    self.csv_saver()
                    self.logger.info("Pause for 3 seconds")
                    time.sleep(3)
        else:
            self.logger.info("Please enter Valid URL")
        self.logger.info("BestSeller Garbage collector: collected %d objects.(END)" % (gc.collect()))

    def search_URL(self,url,kinddleInclude):
        self.kinddleInclude = kinddleInclude
        self.logger.info("Search Product Garbage collector: collected %d objects.(START)" % (gc.collect()))
        if url is not None:
            self.search_nextPagefinder(url)
            if self.search_links is not None:
                for link in self.search_links:
                    self.attribute_getter(link)
                    self.logger.info("Titel of URL = "+self.title)
                    link_review = self.review_productPage(link)
                    if link_review == "Kinndle Excluded":
                        self.logger.info("Excluded kindle page")
                        pass
                    self.review_getter(link_review)
                    self.rating_equalizer()
                    self.csv_saver()
                    self.logger.info("Pause for 3 seconds")
                    time.sleep(3)
        else:
            self.logger.info("Please enter Valid URL")
        self.logger.info("Search Product Garbage collector: collected %d objects.(END)" % (gc.collect()))
amazon = Amazon()
amazon.product_URL("https://www.amazon.in/B11-Extra-Handled-Sturdy-Weight/dp/B01MD18PBI/ref=sr_1_2?dchild=1&keywords=shoe+horn&qid=1585478999&sr=8-2")