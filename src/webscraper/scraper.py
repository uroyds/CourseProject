from bs4 import BeautifulSoup

import re 
import urllib
import time
import json


import requests

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options


#uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url,driver):
    driver.get(url)
    time.sleep(5) # give it some time
    res_html = driver.execute_script('return document.body.innerHTML')
    with open("base_test.html", 'w') as base:
        base.write(res_html)

    soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
    return soup

def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup

# basic webscraper that retrieves data from coursera using the

# set session with coursera
def start_coursera_session(auth_cookie):
    session = requests.Session()

    session.cookies.set('CAUTH', auth_cookie)
    return session


def get_cauth():
    with open("cauth_cookie.txt","r") as f:
        auth_cookie = f.read()

    return auth_cookie

# test using resquests
def test():

    session =  start_coursera_session(get_cauth())

    url = "https://www.coursera.org/learn/text-retrieval/lecture/rLpwp/lesson-1-1-natural-language-content-analysis"
    request = session.get(url)

    with open("base_test.html", 'w') as base:
        base.write(request.text)
    
    soup = BeautifulSoup(request.text, "html.parser")

    data = soup.find_all('div', {"class" : "phrases"})
    print(data)

# test using selenium
def test2():
    options = Options()
    options.headless = True
    
    
    # initialize chrome driver
    cauth = get_cauth()
    driver = webdriver.Chrome('./chromedriver',options=options)
    driver.get("https://www.coursera.org")
    driver.add_cookie({"name": "CAUTH", "value": cauth})

    url = "https://www.coursera.org/learn/text-retrieval/lecture/rLpwp/lesson-1-1-natural-language-content-analysis"
    
    soup = get_js_soup(url, driver)
    data = soup.find_all('div', {"class" : "phrases"})
    print(data) 

def main():
    pass

if __name__ == '__main__':
    test2()