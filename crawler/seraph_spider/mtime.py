#-*- coding: utf-8 -*-
__author__ = 'seraph'
import gevent
from gevent import monkey
monkey.patch_all()
import os
import sys
selfpath = os.path.split(os.path.realpath(__file__))[0]
PATH = os.path.abspath(os.path.join(selfpath,'..'))
sys.path.append(PATH)
from crawler import settings          #your project settings file
from django.core.management import setup_environ     #environment setup function
setup_environ(settings)
from spider.models import Car
import requests
import lxml.html
from lxml.html.clean import Cleaner
import logging
import logging.config
import re
logging.config.fileConfig('crawler/seraph_spider/logging.conf')
logger = logging.getLogger('autohome')

reload(sys)
sys.setdefaultencoding('utf-8')


cleaner = Cleaner(style=True,scripts=True,page_structure=False,safe_attrs_only=True,safe_attrs=['src'],kill_tags=['script'])

def spiderboy(url):
    page = requests.get(url)
    html = lxml.html.fromstring(page.content)
    items = html.cssselect('.news_lists li')
    for item in items:
        car_link = item.cssselect('a')[0].get('href')
        logger.info('link: '+car_link)
        try:
            Car.objects.get(car_link=car_link)
            logger.info('already have ' + car_link)
            pass
        except:
            car_title = str(item.cssselect('a')[0].text_content())
            logger.info('title: '+car_title)
            car_icon = 'http://www.yooeasy.com/wp-content/uploads/2010/07/mtime-logo.jpg'
            car_des = ''

            innerpage = requests.get(car_link)
            innerhtml = lxml.html.fromstring(innerpage.content)

            try:
                next = innerhtml.cssselect('.next')[0].get('href')
            except:
                next = None

            #if next:




























