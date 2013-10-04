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
import re
reload(sys)
sys.setdefaultencoding('utf-8')

cleaner = Cleaner(style=True,scripts=True,page_structure=False,safe_attrs_only=True,safe_attrs=['src'],kill_tags=['a'])




base_url = 'http://www.527motor.com/'

def spiderboy(cate):

    page = requests.get(cate)
    html = lxml.html.fromstring(page.content)

    items = html.cssselect('.bbda')

    for item in items:
        car_link = base_url + item.cssselect('.xs2 a')[0].get('href')
        try:
            Car.objects.get(car_link=car_link)
            pass
        except Exception,e:
            car_title = str(item.cssselect('.xs2 a')[0].text_content())
            car_icon = base_url + item.cssselect('.atc img')[0].get('src')
            car_des = str(item.cssselect('.atc')[0].text_content())

            innerpage = requests.get(car_link)
            innerhtml = lxml.html.fromstring(innerpage.content)
            writer = lxml.html.tostring(innerhtml.cssselect('.xg1')[0])

            mid_body = lxml.html.tostring(innerhtml.cssselect('#article_content')[0])
            pattern = re.compile(r'src="')

            pattern2 = re.compile(r'href="')
            ins = 'src="'+base_url
            ins2 = 'href="'+base_url

            mid_body = pattern.sub(ins,mid_body)
            mid_body = pattern2.sub(ins2,mid_body)

            car_body = writer+mid_body

            ca = Car(car_title=car_title,
                     car_des=car_des,
                     car_link=car_link,
                     car_body=car_body,
                     car_icon=car_icon,
                     car_source="527motor",
                     car_cate='motorbike')

            ca.save()


if __name__ == '__main__':
    gevent.joinall(
        [
            gevent.spawn(spiderboy,('http://www.527motor.com/portal.php?mod=list&catid=2')),
            gevent.spawn(spiderboy,('http://www.527motor.com/portal.php?mod=list&catid=58')),
            gevent.spawn(spiderboy,('http://www.527motor.com/portal.php?mod=list&catid=60')),
            gevent.spawn(spiderboy,('http://www.527motor.com/portal.php?mod=list&catid=62')),
        ]
    )



