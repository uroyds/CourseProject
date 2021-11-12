from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

import time
import json
import os
from collections import deque

from urllib import parse

from pathlib import Path

import re

class Coursera:

    def __init__(self, cauth, download_path = "."):

        options = Options()
        options.headless = True
        options.add_argument('--log-level=2')

        # for webcrawling
        self.crawl_stack = deque()
        self.current_page = "https://www.coursera.org"


        self.driver = webdriver.Chrome('./chromedriver',options=options)
        self.driver.get("https://www.coursera.org")
        self.driver.add_cookie({"name": "CAUTH", "value": cauth})

        # set download path
        self.download_path = download_path

    # downloads all the lectures for a class
    def download_class(self, class_name):
        # need to navigate to welcome page? 

        class_home_page = f'https://www.coursera.org/learn/{class_name}/home/welcome'

        #print(class_home_page)

        #crawl_stack = deque()
        #crawl_stack.append(class_home_page)
        # check for rc-WeekCollectionNavigationItem to get weeks?
        home_soup = self.get_html_soup(class_home_page, 5)

        weeks = self.parse_home_page(home_soup)


        for week in weeks:
            #print(week_url)
            self.download_week(week)
            # for each week get lecture 
                # for each lecture parse

    def download_week(self, week_url):
        pass
        week_soup = self.get_html_soup(week_url, 5)

        lectures = self.parse_week_page(week_soup)

        for lecture in lectures:
            print(lecture)
            #self.download_lecture(lecture)


    # downloads a lecture given its class na
    #def download_lecture(self, url)
    def download_lecture(self, lecture_url):
    
        # construct lecture url
        url = parse.urlparse(lecture_url)

        class_name = ""
        lecture_name = ""

        if re.match("\/learn\/.+\/lecture\/.+", url.path):
            url_path_directory = url.path.strip('/').split('/')
            class_name = url_path_directory[1]
            lecture_name = url_path_directory[-1]
        else:
            print("Invalid lecture URL")
            return

        soup = self.get_html_soup(lecture_url, 5)

        video_link, lecture_timestamp, lecture_data = self.parse_lecture(soup)



        
        download_directory = os.path.join(self.download_path, class_name)
        download_path = os.path.join(download_directory, lecture_name + ".txt")

        download_path = os.path.join(self.download_path, lecture_name + ".txt")
        # write downloaded to file
        with open(download_path,"w") as f:
            # video_link at the start of file?
            #f.write(video_link + '\n')
            for j in range(len(lecture_data)):
                f.write(lecture_timestamp[j] + " : " + lecture_data[j] + "\n")

    
    def get_html_soup(self, url, delay = 1):
        self.driver.get(url)
        time.sleep(delay) # give it some time
        res_html = self.driver.execute_script('return document.body.innerHTML')

        with open("test.html", 'w') as h:
            h.write(res_html)
        soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content

        return soup


            
    # given a link pass it to other function
    def handle_link(self, link):
        
        lecture_re = re.compile
        some_url = parse.urlparse(link)
        print(some_url)
        # insite move
        if some_url.netloc == "":
            some_url = some_url._replace(scheme="https", netloc="www.coursera.org")
            path = some_url.path.split('/')
            # path should be format  learn/{class_name}/{page_type}/*
            if re.match("\/learn\/"):
                # download lecture
                print(some_url)
                pass
                # download_lecture()

            elif path[3] == "home":
                # searchable page for more links
                print(some_url)
                pass


    # look for links to the weeks
    def parse_home_page(self, soup):
        nav_weeks = soup.find_all('a', {"data-click-key" : "open_course_home.menu.click.nav_week"})

        weeks_url = []

        for w in nav_weeks:
            url = parse.urljoin("https://www.coursera.org", w.get('href'))
            weeks_url.append(url)

        return weeks_url


    # look for links to the lecture in each week
    def parse_week_page(self, soup):
        
        links = soup.find_all('a', {'data-click-key' : 'open_course_home.period_page.click.item_link'})

        lecture_urls = []
        for l in links:
            # filter for lectures
            path = l.get('href')
            if re.match("\/learn\/.+\/lecture\/.+", path):
                url = parse.urljoin("https://www.coursera.org", path)
                lecture_urls.append(url)

        return lecture_urls

    # parses lecture webpage for information
    def parse_lecture(self, soup):
        
        video_link = soup.find('video').get("src")

        timestamps = soup.find_all('button',{"class" : "timestamp"})
        data = soup.find_all('div', {"class" : "phrases"})

        text_timestamp = [t.contents[1] for t in timestamps]
        text_data = [d.text for d in data]

        # maybe json style
        #time_stamped_text = dict(zip(text_timestamp, text_data))
        #print(time_stamped_text)
        
        return video_link, text_timestamp, text_data
