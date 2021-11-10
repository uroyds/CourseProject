from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

from api import Coursera


def get_cauth():
    with open("cauth_cookie.txt","r") as f:
        auth_cookie = f.read()

    return auth_cookie



def main():
    
    cauth = get_cauth()

    session = Coursera(cauth)

    session.download_class("text-retrieval", ".")


# downloads 1 lecture
def test():

    cauth = get_cauth()

    session = Coursera(cauth)

    session.download_lecture('text-retrieval', 'lesson-1-1-natural-language-content-analysis', 'rLpwp')

if __name__ == '__main__':
    test()