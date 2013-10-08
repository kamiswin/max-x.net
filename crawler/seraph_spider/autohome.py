__author__ = 'seraph'

autohome_url = ''
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
logger = logging.getLogger('neeu')

reload(sys)
sys.setdefaultencoding('utf-8')


cleaner = Cleaner(style=True,scripts=True,page_structure=False,safe_attrs_only=False,kill_tags=['script','a'])

def spiderboy(url):

    page = requests.get(url)
    html = lxml.html.fromstring(page.content.decode('gb2312','ignore'))
    items = html.cssselect('#ATitle')

    for item in items:
        car_link = item.get('href')
        logger.info('link: '+car_link)
        try:
            Car.objects.get(car_link=car_link)
            pass
        except:
            car_title = str(item.text_content())
            logger.info('title: '+car_title)
            car_icon = 'http://x.autoimg.cn/news/index/img/20110801/logo_new.png'
            car_des = ''

            innerpage = requests.get(car_link)
            innerhtml = lxml.html.fromstring(innerpage.content.decode('gb23125','ignore'))

            try:
                next = innerhtml.cssselect('.page-item-readall')[0].get('href')
                wholepage = requests.get(next)
                wholehtml = lxml.html.fromstring(wholepage.content.decode('gb2312','ignore'))

            except:



