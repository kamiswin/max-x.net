#!/usr/bin/env python
# encoding:utf-8
import requests
import re
import lxml.html
import logging
import logging.config
from lxml.html.clean import Cleaner
from crawler import settings
from django.core.management import setup_environ
setup_environ(settings)
from spider.models import Car
logging.config.fileConfig('crawler/seraph_spider/logging.conf')
logger = logging.getLogger(__name__)

cleaner = Cleaner(style=True,scripts=True,page_structure=False,safe_attrs_only=True,safe_attrs=['src'])

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

    def clean(self,car_body):
        r = re.compile(r'<a>|</a>')
        car_body = cleaner.clean_html(car_body)
        car_body = r.sub('',car_body)
        return car_body

        
        
        
