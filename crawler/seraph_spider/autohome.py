#-*- coding: utf-8 -*-
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
logger = logging.getLogger('autohome')

reload(sys)
sys.setdefaultencoding('utf-8')


cleaner = Cleaner(style=True,scripts=True,page_structure=False,safe_attrs_only=True,safe_attrs=['src'],kill_tags=['script'])

def cut(content):
    if u'相关阅读' in content:
        ncontent = content.split('相关阅读')[0]+'</p>'
    elif u'更多阅读' in content:
        ncontent = content.split('更多阅读')[0]+'</p>'
    else:
        ncontent = content


    return ncontent


base_url = 'http://www.autohome.com.cn'

def spiderboy(url):
    page = requests.get(url)
    html = lxml.html.fromstring(page.content.decode('gbk'))
    items = html.cssselect('#ATitle')

    for item in items:
        car_link = item.get('href')
        logger.info('link: '+car_link)
        try:
            Car.objects.get(car_link=car_link)
            logger.info('already have ' + car_link)
            pass
        except:
            car_title = str(item.text_content())
            logger.info('title: '+car_title)
            car_icon = 'http://x.autoimg.cn/news/index/img/20110801/logo_new.png'
            car_des = ''

            innerpage = requests.get(car_link)
            innerhtml = lxml.html.fromstring(innerpage.content.decode('gbk'))

            try:
                next = base_url + innerhtml.cssselect('.page-item-readall')[0].get('href')
            except:
                next = None

            if next:
                innerpage = requests.get(next)
                innerhtml = lxml.html.fromstring(innerpage.content.decode('gbk'))

            try:
                innerhtml.cssselect('.diversion-box')[0].drop_tree()
            except:
                pass

            try:
                innerhtml.cssselect('.btn.font-normal')[0].drop_tree()
            except:
                pass


            article = innerhtml.cssselect('#articleContent')[0]
            mid_body = lxml.html.tostring(article,encoding=unicode)
            mid_body2 = cut(mid_body)
            r = re.compile(r'<a>|</a>')
            mid_body3 = cleaner.clean_html(mid_body2)
            car_body = mid_body3
            car_body = r.sub('',car_body)

            ca = Car(car_title=car_title,
                     car_des=car_des,
                     car_link=car_link,
                     car_body=car_body,
                     car_icon=car_icon,
                     car_source="autohome",
                     car_cate='car')

            ca.save()
            logger.info('done one')

if __name__ == '__main__':
    gevent.joinall(
        [
            gevent.spawn(spiderboy,('http://www.autohome.com.cn/list/c71-1.html')),
            gevent.spawn(spiderboy,('http://www.autohome.com.cn/list/c20-1.html')),
            gevent.spawn(spiderboy,('http://www.autohome.com.cn/list/c40-1.html')),
            gevent.spawn(spiderboy,('http://www.autohome.com.cn/list/c62-1.html')),
            gevent.spawn(spiderboy,('http://www.autohome.com.cn/list/c17-1.html')),
        ]
    )
    #spiderboy('http://www.autohome.com.cn/list/c40-1.html')

