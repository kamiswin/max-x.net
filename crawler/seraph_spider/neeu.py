# -*- coding: utf-8 -*-
__author__ = 'max'
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

catechoice = {
    ('http://www.neeu.com/motor/news/info/',
     'http://www.neeu.com/motor/news/launch/',
     'http://www.neeu.com/motor/news/top/',
     'http://www.neeu.com/motor/news/event/',
     'http://www.neeu.com/motor/news/design/',
     'http://www.neeu.com/motor/news/test/',
     'http://www.neeu.com/motor/news/lifestyle/',
    ):'car',
    ('http://www.neeu.com/yacht/news/info/',
     'http://www.neeu.com/yacht/news/luxury/',
     'http://www.neeu.com/yacht/news/event/',
     'http://www.neeu.com/yacht/news/lifestyle/',
     'http://www.neeu.com/yacht/news/sailing/',
     'http://www.neeu.com/yacht/news/elite/',
     'http://www.neeu.com/yacht/news/academy/',
    ):'boat',
    ('http://www.neeu.com/jet/news/info/',
     'http://www.neeu.com/jet/news/aircraft/',
     'http://www.neeu.com/jet/news/industry/',
     'http://www.neeu.com/jet/news/event/',
     'http://www.neeu.com/jet/news/lifestyle/',
     'http://www.neeu.com/jet/news/elite/',
     'http://www.neeu.com/jet/news/academy/',
    ):'plane',
    ('http://www.neeu.com/realestate/news/info/',
     'http://www.neeu.com/realestate/news/architecture/',
     'http://www.neeu.com/realestate/news/star/',
     'http://www.neeu.com/realestate/news/lifestyle/',
     'http://www.neeu.com/realestate/news/event/',
     'http://www.neeu.com/realestate/news/elite/',
     'http://www.neeu.com/realestate/news/guide/',
     'http://www.neeu.com/homedesign/news/info/',
     'http://www.neeu.com/homedesign/news/luxury/',
     'http://www.neeu.com/homedesign/news/trend/',
     'http://www.neeu.com/homedesign/news/event/',
     'http://www.neeu.com/homedesign/news/lifestyle/',
     'http://www.neeu.com/homedesign/news/academy/',
     'http://www.neeu.com/homedesign/news/elite/',
    ):'house',
    ('http://www.neeu.com/Gourmet/news/info/',
     'http://www.neeu.com/gourmet/news/restaurant/',
     'http://www.neeu.com/gourmet/news/delicacy/',
     'http://www.neeu.com/gourmet/news/culture/',
     'http://www.neeu.com/gourmet/news/academy/',
     'http://www.neeu.com/gourmet/news/epicure/',
     'http://www.neeu.com/gourmet/news/event/',
     'http://www.neeu.com/Wine/news/info/',
     'http://www.neeu.com/wine/news/academy/',
     'http://www.neeu.com/wine/news/finest/',
     'http://www.neeu.com/wine/news/elite/',
     'http://www.neeu.com/wine/news/collect-invest/',
     'http://www.neeu.com/wine/news/event/',
     'http://www.neeu.com/wine/news/culture/',
     'http://www.neeu.com/wine/news/chateau/',
    ):'food',
    }

url = [
    'http://www.neeu.com/Gourmet/news/info/',
    'http://www.neeu.com/gourmet/news/restaurant/',
    'http://www.neeu.com/gourmet/news/delicacy/',
    'http://www.neeu.com/gourmet/news/culture/',
    'http://www.neeu.com/gourmet/news/academy/',
    'http://www.neeu.com/gourmet/news/epicure/',
    'http://www.neeu.com/gourmet/news/event/',
    'http://www.neeu.com/Wine/news/info/',
    'http://www.neeu.com/wine/news/academy/',
    'http://www.neeu.com/wine/news/finest/',
    'http://www.neeu.com/wine/news/elite/',
    'http://www.neeu.com/wine/news/collect-invest/',
    'http://www.neeu.com/wine/news/event/',
    'http://www.neeu.com/wine/news/culture/',
    'http://www.neeu.com/wine/news/chateau/',
    'http://www.neeu.com/realestate/news/info/',
    'http://www.neeu.com/realestate/news/architecture/',
    'http://www.neeu.com/realestate/news/star/',
    'http://www.neeu.com/realestate/news/lifestyle/',
    'http://www.neeu.com/realestate/news/event/',
    'http://www.neeu.com/realestate/news/elite/',
    'http://www.neeu.com/realestate/news/guide/',
    'http://www.neeu.com/homedesign/news/info/',
    'http://www.neeu.com/homedesign/news/luxury/',
    'http://www.neeu.com/homedesign/news/trend/',
    'http://www.neeu.com/homedesign/news/event/',
    'http://www.neeu.com/homedesign/news/lifestyle/',
    'http://www.neeu.com/homedesign/news/academy/',
    'http://www.neeu.com/homedesign/news/elite/',
    'http://www.neeu.com/jet/news/info/',
    'http://www.neeu.com/jet/news/aircraft/',
    'http://www.neeu.com/jet/news/industry/',
    'http://www.neeu.com/jet/news/event/',
    'http://www.neeu.com/jet/news/lifestyle/',
    'http://www.neeu.com/jet/news/elite/',
    'http://www.neeu.com/jet/news/academy/',
    'http://www.neeu.com/yacht/news/info/',
    'http://www.neeu.com/yacht/news/luxury/',
    'http://www.neeu.com/yacht/news/event/',
    'http://www.neeu.com/yacht/news/lifestyle/',
    'http://www.neeu.com/yacht/news/sailing/',
    'http://www.neeu.com/yacht/news/elite/',
    'http://www.neeu.com/yacht/news/academy/',
    'http://www.neeu.com/motor/news/info/',
    'http://www.neeu.com/motor/news/launch/',
    'http://www.neeu.com/motor/news/top/',
    'http://www.neeu.com/motor/news/event/',
    'http://www.neeu.com/motor/news/design/',
    'http://www.neeu.com/motor/news/test/',
    'http://www.neeu.com/motor/news/lifestyle/',
]

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip,deflate,sdch',
    'Accept-Language':'en-US,en;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'www.neeu.com',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36',
}

cleaner = Cleaner(style=True,scripts=True,page_structure=False,safe_attrs_only=False,kill_tags=['script','a'])

def category_select(item,dic):
    for i in dic.iterkeys():
        if item in i:
            return dic.get(i)

def nextPage(html,base_url=''):
    #print 111
    logger.info('have many page')
    car_body = lxml.html.tostring(html.cssselect('.content')[0])
    car_body = cleaner.clean_html(car_body)
    while html.cssselect('.cpagesizebottom a')[-1].text_content() == u'下一页':
        #print 222
        #print html.cssselect('.cpagesizebottom a')[0].get('href')
        nextpage = requests.get(base_url + html.cssselect('.cpagesizebottom a')[-1].get('href'),headers=headers)
        #print 333
        nexthtml = lxml.html.fromstring(nextpage.content.decode('gbk','ignore'))
        #print 444
        body = lxml.html.tostring(nexthtml.cssselect('.content')[0])
        #print 555
        body = cleaner.clean_html(body)
        #print 666
        car_body += body
        #print 777
        html = nexthtml
        #print 888
    #print 999
    return car_body


def spiderboy(url):

    page = requests.get(url,headers=headers)
    base_url ='/'.join(page.url.split('/')[:-4])

    html = lxml.html.fromstring(page.content.decode('gbk','ignore'))
    items = html.cssselect('.anewsnotitle')
    for item in items:
        car_link = base_url + item.cssselect('.newstext h3 a')[0].get('href')
        # logger.info('link: '+car_link)
        print car_link
        car_title = str(item.cssselect('.newstext h3 a')[0].text_content())
        try:
            Car.objects.get(car_title=car_title)
            pass
        except Exception,e:
            
            # logger.info('title: '+car_title)
            car_icon = base_url + item.cssselect('.newspic a img')[0].get('src')
            # logger.info('icon_url: '+car_icon)
            car_des = str(item.cssselect('.newstext p')[0].text_content())
            # logger.info('get des')

            innerpage = requests.get(car_link,headers=headers)
            innerhtml = lxml.html.fromstring(innerpage.content.decode('gbk','ignore'))

            try:
                next = innerhtml.cssselect('.cpagesizebottom a')[-1]
                if next.text_content() == u'下一页':
                    mid_body = nextPage(innerhtml,base_url)
                else:
                    mid_body = lxml.html.tostring(innerhtml.cssselect('.content')[0])
                    mid_body = cleaner.clean_html(mid_body)

            except:
                mid_body = lxml.html.tostring(innerhtml.cssselect('.content')[0])
                mid_body = cleaner.clean_html(mid_body)

            pattern = re.compile(r'(?:src|href)="([^http].*?[\.jpg])"', re.VERBOSE)

            test = pattern.findall(mid_body)
            test = list(set(test))

            for i in test:
                mid_body = mid_body.replace(i,base_url+i)

            car_body = mid_body
            # logger.info('body: catch')
            car_cate = category_select(url,catechoice)
            # logger.info('category: '+car_cate)

            ca = Car(car_title=car_title,
                     car_des=car_des,
                     car_link=car_link,
                     car_body=car_body,
                     car_icon=car_icon,
                     car_source="neeu",
                     car_cate=car_cate)


            ca.save()
            logger.info('done one')



def ll1():
    for i in url[0:10]:
        spiderboy(i)

def ll2():
    for i in url[10:20]:
        spiderboy(i)

def ll3():
    for i in url[20:30]:
        spiderboy(i)

def ll4():
    for i in url[30:40]:
        spiderboy(i)

def ll5():
    for i in url[40:50]:
        spiderboy(i)


if __name__ == '__main__':
    gevent.joinall(
        [
            gevent.spawn(ll1),
            gevent.spawn(ll2),
            gevent.spawn(ll3),
            gevent.spawn(ll4),
            gevent.spawn(ll5),
            ]
    )


