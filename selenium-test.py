__author__ = 'seraph'
from selenium import webdriver
from selenium.webdriver import ActionChains
from time import sleep

dr = webdriver.Firefox()
actdr = ActionChains(dr)



dr.get('http://www.favbuy.com')

el = dr.find_elements_by_css_selector('.nav-item')[1]

actdr.move_to_element(el).perform()

sleep(10)

if dr is not None:
    dr.quit()