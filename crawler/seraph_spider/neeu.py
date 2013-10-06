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
#from lxml.html.clean import Cleaner
import logging
import logging.config

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
def category_select(item,dic):
    for i in dic.iterkeys():
        if item in i:
            return dic.get(i)


def nextPage(html,base_url=''):
    logger.info('have many page')
    car_body = lxml.html.tostring(html.cssselect('.content')[0])
    while html.cssselect('.cpagesizebottom a')[-1].text_content() == u'下一页':
        nextpage = requests.get(base_url + html.cssselect('.cpagesizebottom a')[0].get('href'))
        nexthtml = lxml.html.fromstring(nextpage.content)
        body = lxml.html.tostring(nexthtml.cssselect('.content')[0])
        car_body += body
        html = nexthtml
    return car_body

def spiderboy(url):

    page = requests.get(url)
    base_url ='/'.join(page.url.split('/')[:-4])

    html = lxml.html.fromstring(page.content)
    items = html.cssselect('.anewsnotitle')
    for item in items:
        car_link = base_url + item.cssselect('.newstext h3 a')[0].get('href')
        logger.info('link: '+car_link)
        try:
            car_bo = Car.objects.get(car_link = car_link)
            pass
        except Exception,e:
            car_title = str(item.cssselect('.newstext h3 a')[0].text_content())
            logger.info('title: '+car_title)
            car_icon = base_url + item.cssselect('.newspic a img')[0].get('src')
            logger.info('icon_url: '+car_icon)
            car_des = str(item.cssselect('.newstext p')[0].text_content())
            logger.info('get des')

            innerpage = requests.get(car_link)
            innerhtml = lxml.html.fromstring(innerpage.content)

            try:
                next = innerhtml.cssselect('.cpagesizebottom a')[-1]
                if next.text_content() == u'下一页':
                    mid_body = nextPage(innerhtml,base_url)
                else:
                    mid_body = lxml.html.tostring(innerhtml.cssselect('.content')[0])

            except:
                mid_body = lxml.html.tostring(innerhtml.cssselect('.content')[0])



            car_body = mid_body
            logger.info('body: catch')
            car_cate = category_select(url,catechoice)
            logger.info('category: '+car_cate)

            ca = Car(car_title=car_title,
                     car_des=car_des,
                     car_link=car_link,
                     car_body=car_body,
                     car_icon=car_icon,
                     car_source="neeu",
                     car_cate=car_cate)


            ca.save()
            logger.info('done one')


if __name__ == '__main__':
    gevent.joinall(
        [
            gevent.spawn(spiderboy,(url[1])),
            gevent.spawn(spiderboy,(url[2])),
            gevent.spawn(spiderboy,(url[3])),
            gevent.spawn(spiderboy,(url[4])),
            gevent.spawn(spiderboy,(url[5])),
            gevent.spawn(spiderboy,(url[6])),
            gevent.spawn(spiderboy,(url[7])),
            gevent.spawn(spiderboy,(url[8])),
            gevent.spawn(spiderboy,(url[9])),
            gevent.spawn(spiderboy,(url[10])),
            gevent.spawn(spiderboy,(url[11])),
            gevent.spawn(spiderboy,(url[12])),
            gevent.spawn(spiderboy,(url[13])),
            gevent.spawn(spiderboy,(url[14])),
            gevent.spawn(spiderboy,(url[15])),
            gevent.spawn(spiderboy,(url[16])),
            gevent.spawn(spiderboy,(url[17])),
            gevent.spawn(spiderboy,(url[18])),
            gevent.spawn(spiderboy,(url[19])),
            gevent.spawn(spiderboy,(url[20])),
            gevent.spawn(spiderboy,(url[21])),
            gevent.spawn(spiderboy,(url[22])),
            gevent.spawn(spiderboy,(url[23])),
            gevent.spawn(spiderboy,(url[24])),
            gevent.spawn(spiderboy,(url[25])),
            gevent.spawn(spiderboy,(url[26])),
            gevent.spawn(spiderboy,(url[27])),
            gevent.spawn(spiderboy,(url[28])),
            gevent.spawn(spiderboy,(url[29])),
            gevent.spawn(spiderboy,(url[30])),
            gevent.spawn(spiderboy,(url[31])),
            gevent.spawn(spiderboy,(url[32])),
            gevent.spawn(spiderboy,(url[33])),
            gevent.spawn(spiderboy,(url[34])),
            gevent.spawn(spiderboy,(url[35])),
            gevent.spawn(spiderboy,(url[36])),
            gevent.spawn(spiderboy,(url[37])),
            gevent.spawn(spiderboy,(url[38])),
            gevent.spawn(spiderboy,(url[39])),
            gevent.spawn(spiderboy,(url[40])),
            gevent.spawn(spiderboy,(url[41])),
            gevent.spawn(spiderboy,(url[42])),
            gevent.spawn(spiderboy,(url[43])),
            gevent.spawn(spiderboy,(url[44])),
            gevent.spawn(spiderboy,(url[45])),
            gevent.spawn(spiderboy,(url[46])),
            gevent.spawn(spiderboy,(url[47])),
            gevent.spawn(spiderboy,(url[48])),
            gevent.spawn(spiderboy,(url[49])),
            gevent.spawn(spiderboy,(url[0])),
            ]
    )


