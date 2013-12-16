# -*- coding: utf-8 -*-
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
logger = logging.getLogger('chinaluxus')


reload(sys)
sys.setdefaultencoding('utf-8')


catechoice = {
    ('http://drive.chinaluxus.com/Car',
     'http://drive.chinaluxus.com/Lif',
     'http://drive.chinaluxus.com/Cul',
     'http://drive.chinaluxus.com/Gal'
    ):'car',
    ('http://drive.chinaluxus.com/Yac',
    ):'boat',
    ('http://drive.chinaluxus.com/Air',
    ):'plane',
    ('http://re.chinaluxus.com/Eli/',
     'http://re.chinaluxus.com/Tre/',
     'http://re.chinaluxus.com/Hom/',
     'http://re.chinaluxus.com/Dsg/',
     'http://re.chinaluxus.com/Cel/',
    ):'house',
    ('http://taste.chinaluxus.com/Sca/',
     'http://taste.chinaluxus.com/Drk/',
     'http://taste.chinaluxus.com/Fod/',
    ):'food',
    }

def category_select(item,dic):
    for i in dic.iterkeys():
        if item in i:
            return dic.get(i)




cleaner = Cleaner(style=True,scripts=True,page_structure=False,safe_attrs_only=True,safe_attrs=['src'])

def spiderboy(cate):
    page = requests.get(cate)
    html = lxml.html.fromstring(page.content)
    for item in html.cssselect('.listDetail'):
        car_link=item.cssselect('.fb14d a')[0].get('href')
        car_title=str(item.cssselect('.fb14d')[0].text_content())
        # logger.info('link: ' + car_link)
        print 'link '+car_link
        try:
            Car.objects.get(car_title=car_title)
            # logger.info('already have '+ car_link)
            print 'already have '+ car_link
            pass
        except Exception, e:

            
            # logger.info('title: '+car_title)
            print 'title '+car_title
            # 中奢网的汽车快讯栏目么有图片
            try:
                car_icon=item.cssselect('.img img')[0].get('src')
            except Exception, e:
                # logger.warn('have no : '+car_icon)
                print 'have no '+car_icon
                car_icon='/static/img/a1.jpg'

            car_des=str(item.cssselect('.spanText')[0].text_content())
            # logger.info('des: '+car_des)

            innerpage = requests.get(car_link)
            innerhtml = lxml.html.fromstring(innerpage.content)

            base_url = '/'.join(innerpage.url.split('/')[:-1])+'/'

            chinaluxus_boo = innerhtml.cssselect('.text')[-1]
            mid_body = lxml.html.tostring(chinaluxus_boo)
            if chinaluxus_boo.text_content() == u'支持度':
                chinaluxus_boo = innerhtml.cssselect('.explainPic')[0]
                mid_body = lxml.html.tostring(chinaluxus_boo)
            if len(innerhtml.cssselect('.next')) > 0 and len(innerhtml.cssselect('.nextBtn')) == 0:
                mid_body = nextPage(innerhtml,base_url=base_url)
            if len(innerhtml.cssselect('.nextBtn')) > 0:
                mid_body = nextPhoto(innerhtml)


            car_body =mid_body
            # logger.info('body: catch')
            car_cate = category_select(cate,catechoice)
            # logger.info('category: '+car_cate)

            r = re.compile(r'<a>|</a>')
            car_body = cleaner.clean_html(car_body)
            car_body = r.sub('',car_body)


            ca = Car(car_title=car_title,
                     car_des=car_des,
                     car_link=car_link,
                     car_body=car_body,
                     car_icon=car_icon,
                     car_source="chinaluxus",
                     car_cate=car_cate)


            ca.save()
            # logger.info('done one')




def nextPage(html,base_url=''):
    # logger.info('have many page')
    car_body = lxml.html.tostring(html.cssselect('.text')[-1])
    while len(html.cssselect('.next')) > 0 and len(html.cssselect('.nextBtn')) == 0:
        nextpage = requests.get(base_url + html.cssselect('.next')[0].get('href'))
        nexthtml = lxml.html.fromstring(nextpage.content)
        body = lxml.html.tostring(nexthtml.cssselect('.text')[-1])
        car_body += body
        html = nexthtml
    return car_body

def nextPhoto(html):
    # logger.info('have many photo')
    last_url=''
    up_photo = lxml.html.tostring(html.cssselect('.destinPic img')[0])
    up_body = lxml.html.tostring(html.cssselect('.explainPic')[0])
    up_whole = up_photo + up_body
    car_body = up_whole
    while len(html.cssselect('.nextBtn')) > 0:
        if str(html.cssselect('.nextBtn')[0].get('href')) != str(last_url):
            try:
                nextpage = requests.get(html.cssselect('.nextBtn')[0].get('href'))
                nexthtml = lxml.html.fromstring(nextpage.content)
                last_url = nextpage.url
                try:
                    photo = lxml.html.tostring(nexthtml.cssselect('.desImg')[0])
                    body = lxml.html.tostring(nexthtml.cssselect('.explainPic')[0])
                    wholebody = photo+body
                    car_body += wholebody
                except Exception, e:
                    car_body = '操 阴我'
                html = nexthtml
            except Exception,e:
                pass
        else:
            break
    return car_body




if __name__ == '__main__':
    gevent.joinall(
        [
            gevent.spawn(spiderboy,('http://drive.chinaluxus.com/Car')),
            gevent.spawn(spiderboy,('http://drive.chinaluxus.com/Lif')),
            gevent.spawn(spiderboy,('http://drive.chinaluxus.com/Cul')),
            gevent.spawn(spiderboy,('http://drive.chinaluxus.com/Gal')),
            gevent.spawn(spiderboy,('http://drive.chinaluxus.com/Yac')),
            gevent.spawn(spiderboy,('http://drive.chinaluxus.com/Air')),
            gevent.spawn(spiderboy,('http://re.chinaluxus.com/Eli/')),
            gevent.spawn(spiderboy,('http://re.chinaluxus.com/Tre/')),
            gevent.spawn(spiderboy,('http://re.chinaluxus.com/Hom/')),
            gevent.spawn(spiderboy,('http://re.chinaluxus.com/Dsg/')),
            gevent.spawn(spiderboy,('http://re.chinaluxus.com/Cel/')),
            gevent.spawn(spiderboy,('http://taste.chinaluxus.com/Fod/')),
            gevent.spawn(spiderboy,('http://taste.chinaluxus.com/Drk/')),
            gevent.spawn(spiderboy,('http://taste.chinaluxus.com/Sca/')),
            ]
    )

    #spiderboy('http://drive.chinaluxus.com/Yac')

