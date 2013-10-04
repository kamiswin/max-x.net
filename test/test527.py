# -*- coding: utf-8 -*-
__author__ = 'max'




import requests
import lxml.html
from lxml.html.clean import Cleaner
import sys
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

        car_link = base_url+item.cssselect('.xs2 a')[0].get('href')
        #print car_link
        car_title = str(item.cssselect('.xs2 a')[0].text_content())
        car_icon = base_url+item.cssselect('.atc img')[0].get('src')
        car_des = str(item.cssselect('.atc')[0].text_content())

        innerpage = requests.get(car_link)
        innerhtml = lxml.html.fromstring(innerpage.content)
        writer = lxml.html.tostring(innerhtml.cssselect('.xg1')[0])
        mid_body = lxml.html.tostring(innerhtml.cssselect('#article_content')[0])
        pattern = re.compile(r'src="')
        ins = 'src="'+base_url

        mid_body = pattern.sub(ins,mid_body)
        car_body = writer+mid_body

        print car_title
        print car_link
        print car_body
        print car_des
        print car_icon


if __name__ == '__main__':
    spiderboy('http://www.527motor.com/portal.php?mod=list&catid=2')



