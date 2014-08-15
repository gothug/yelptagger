from bs4 import BeautifulSoup
from selenium import webdriver
import time

class Crawler:
    def __init__(self):
        self.browser       = webdriver.Firefox()
        self.action_chains = webdriver.ActionChains

    def get_yelp_data(self, url):
        yelp_data = []

        data = self.__get_page_data(url, 60)
        yelp_data.extend(data)

        page_offset = 1
        data_length = len(data)

        while ((data_length > 0) and (page_offset < 1000000)):
            data = self.__get_page_data(\
                url + '?start=' + str(page_offset * 40), 5)
            yelp_data.extend(data)
            data_length = len(data)
            page_offset = page_offset + 1

        return yelp_data

    def __get_page_data(self, url, timeout):
        self.__open_url(url, timeout)

        yelp_data = self.browser.find_elements_by_xpath(\
            '//p[starts-with(@class, "review_comment")]')

        return map(lambda x: x.text, yelp_data)

    def __open_url(self, url, timeout):
        self.browser.get(url)
        print "Please enter capture, if requested.. (you have", timeout,\
            "seconds)"
        time.sleep(timeout)
        print "Proceeding further.."
