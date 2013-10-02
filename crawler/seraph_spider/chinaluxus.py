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



reload(sys)
sys.setdefaultencoding('utf-8')


catechoice = {
    ('Car','Lif','Cul','Gal'):'car',
    ('Yac',):'boat',
    ('Air',):'plane',
}

def category_select(item,dic):
    for i in dic.iterkeys():
        if item in i:
            return dic.get(i)



chinaluxus_url = 'http://drive.chinaluxus.com/'

cleaner = Cleaner(style=True,scripts=True,page_structure=False,safe_attrs_only=True,safe_attrs=['src'],kill_tags=['a'])
def spiderboy(cate):


    page = requests.get(chinaluxus_url+cate)
    html = lxml.html.fromstring(page.content)
    for item in html.cssselect('.listDetail')[1:]:
        car_link=item.cssselect('.fb14d a')[0].get('href')
        try:
            Car.objects.get(car_link=car_link)
            pass
        except Exception, e:

            car_title=str(item.cssselect('.fb14d')[0].text_content())
            # 中奢网的汽车快讯栏目么有图片
            try:
                car_icon=item.cssselect('.img img')[0].get('src')
            except Exception, e:
                car_icon='/static/img/a1.jpg'

            car_des=str(item.cssselect('.spanText')[0].text_content())
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

            car_cate = category_select(cate,catechoice)


            car_body = cleaner.clean_html(car_body)

            ca = Car(car_title=car_title,
                     car_des=car_des,
                     car_link=car_link,
                     car_body=car_body,
                     car_icon=car_icon,
                     car_source="中奢网",
                     car_cate=car_cate)



            ca.save()




def nextPage(html,base_url=''):
    car_body = lxml.html.tostring(html.cssselect('.text')[-1])
    while len(html.cssselect('.next')) > 0 and len(html.cssselect('.nextBtn')) == 0:
        nextpage = requests.get(base_url + html.cssselect('.next')[0].get('href'))
        nexthtml = lxml.html.fromstring(nextpage.content)
        body = lxml.html.tostring(nexthtml.cssselect('.text')[-1])
        car_body += body
        html = nexthtml
    return car_body

def nextPhoto(html):
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
            gevent.spawn(spiderboy,('Car')),
            gevent.spawn(spiderboy,('Lif')),
            gevent.spawn(spiderboy,('Cul')),
            gevent.spawn(spiderboy,('Gal')),
            gevent.spawn(spiderboy,('Yac')),
            gevent.spawn(spiderboy,('Air')),
        ]
    )



