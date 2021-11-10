from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

import time

import json
import os
from pathlib import Path


class Coursera:

    def __init__(self, cauth):

        options = Options()
        options.headless = True
        options.add_argument('--log-level=2')

        self.driver = webdriver.Chrome('./chromedriver',options=options)
        self.driver.get("https://www.coursera.org")
        self.driver.add_cookie({"name": "CAUTH", "value": cauth})


        # test to see if it can login?
    
    # downloads all the lectures for a class
    def download_class(self, class_name, download_directory = "."):
        pass

    # checks to see if it can find the lectures for this class
    def class_lookup(self, class_name):
        pass

    # downloads a lecture given its class na
    def download_lecture(self, class_name, lecture_name, lecture_id, download_directory):
        
        # construct lecture url
        lecture_url = f'https://coursera.org/learn/{class_name}/lecture/{lecture_id}/{lecture_name}'


        soup = get_lecture(lecture_url)

        video_link, lecture_timestamp, lecture_data = parse_lecture(soup)


        # constructe lecture path
        download_path = f"{download_directory}/{class_name}/{lecture_name}.txt"
        
        # write downloaded to file
        with open(download_path,"w") as f:
            # video_link at the start of file?
            #f.write(video_link + '\n')
            for j in range(len(lecture_data)):
                f.write(lecture_timestamp[j] + " : " + lecture_data[j] + "\n")

    
    def get_lecture(self, lecture_url):
        driver.get(url)
        time.sleep(5) # give it some time
        res_html = driver.execute_script('return document.body.innerHTML')

        soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content

        return soup


# parses lecture webpage for information

    def parse_lecture(self, lecture_soup):
        
        video_link = soup.find('video').get("src")

        timestamps = soup.find_all('button',{"class" : "timestamp"})
        data = soup.find_all('div', {"class" : "phrases"})

        text_timestamp = [t.contents[1] for t in timestamps]
        text_data = [d.text for d in data]

        return video_link, text_timestamp, text_data
