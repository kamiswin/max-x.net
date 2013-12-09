#!/usr/bin/env python
# encoding:utf-8
import os
import sys
selfpath = os.path.split(os.path.realpath(__file__))[0]
PATH = os.path.abspath(os.path.join(selfpath, '..'))
sys.path.append(PATH)
import requests
import re
import lxml.html
from lxml.html.clean import Cleaner
from crawler import settings
from django.core.management import setup_environ
setup_environ(settings)
from spider.models import Car
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as WW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


selfpath = os.path.split(os.path.realpath(__file__))[0]
phantompath = selfpath + '/phantomJS'

cleaner = Cleaner(style=True,scripts=True,page_structure=False,safe_attrs_only=True,safe_attrs=['data-lazy-src'])
cleaner2 = Cleaner(style=True,scripts=True,page_structure=False,safe_attrs_only=True,safe_attrs=['src'])

class BaseCraw(object):

    def __init__(self,url):
        self._url = url
        
    def get_category(self):
        pass

    def get_list(self):
        pass

    def get_list_item(self):
        pass

    def get_details_info(self):
        pass

    def fetch_page(self,url):
        try:
            page = requests.get(url,timeout=30)
            return page
        except:
            try:
                page = requests.get(url,timeout=60)
                return page
            except:
                return None
         

    def locate(self,html,locator):
        try:
            nodes = html.cssselect(locator)
            return nodes
        except:
            try:
                nodes = html.cssselect(locator)
                return nodes
            except:
                return None
            
        
    def fromstring(self,page):
        html = lxml.html.fromstring(page.content)
        return html

    def tostring(self,html):
        page_content = lxml.html.tostring(html)
        return page_content

    def clean(self,car_body,flag=''):
        r = re.compile(r'<a>|</a>')
        if flag == 'lazy':
            car_body = cleaner.clean_html(car_body)
            car_body = r.sub('',car_body)
            car_body = car_body.replace('data-lazy-src','src')
        else:
            car_body = cleaner2.clean_html(car_body)
            car_body = r.sub('',car_body)
            
        return car_body


    def init_dr(self):
        self._dr = webdriver.PhantomJS(phantompath)

    def js_fetch(self,url):

        self.init_dr()

        try:
            self._dr.get(url)
        except:
            self._dr.get(url)



    def findby(self,locate,timeout=30):
        el = WW(self._dr,timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,locate)))
        html = el[0].get_attribute('outerHTML')
        return html

        
        
        
