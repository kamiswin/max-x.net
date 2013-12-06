#!/usr/bin/env python
# encoding:utf-8
import os,sys
selfpath = os.path.split(os.path.realpath(__file__))[0]
PATH = os.path.abspath(os.path.join(selfpath, '..'))
sys.path.append(PATH)
from crawler import settings  # your project settings file
from django.core.management import setup_environ  # environment setup function
setup_environ(settings)
from spider.models import Car
from lxml.html.clean import Cleaner
import logging
import logging.config
from base import BaseCraw
logging.config.fileConfig('crawler/seraph_spider/logging.conf')
logger = logging.getLogger(__name__)

class Caranddrive(BaseCraw):

    def __init__(self,url):
        BaseCraw.__init__(self,url)

    def get_list(self):
        # print self._url
        page = self.fetch_page(self._url)
        html = self.fromstring(page)
        nodes_list = self.locate(html,'ol')
        final_html = self.parse_list(nodes_list,html)
        return final_html

    def parse_list(self,nodes_list,html):
        next_node = self.locate(html,'.future')[-1]
        if next_node.text == u'Older Posts »':
            next_url = next_node.get('href') if next_node.get('href').startswith('http') else self._url + next_node.get('href')
            next_page = self.fetch_page(next_url)
            next_html = self.fromstring(next_page)
            next_nodes_list = self.locate(next_html,'ol')
            nodes_list += next_nodes_list
            self.parse_list(next_html)
        else:
            return nodes_list
            
    def get_list_item(self):
        nodes_list = self.get_list()
        for nodes in nodes_list:
            for node in self.locate(nodes,'li'):
                car_title = self.locate(node,'h1 a')[0].text_content().encode('utf-8')
                print 'car_title',car_title
                car_des = self.locate(node,'div.post')[0].text_content().encode('utf-8')
                print 'car_des',car_des
                car_icon = self.locate(node,'div.post p img')[0].get('src')
                car_link = self.locate(node,'h1.postTitle a')[0].get('href')
                print 'car_link',car_link
                try:
                    car_body = self.get_item_details(car_link)
                except:
                    car_body = ''
                car_source = 'caranddrive'
                car_cate = 'car'
                # car_publish_time = 
                ca = Car(car_title=car_title,
                     car_des=car_des,
                     car_link=car_link,
                     car_body=car_body,
                     car_icon=car_icon,
                     car_source=car_source,
                     car_cate=car_cate)


                ca.save()
                logger.info('done one')


    def get_item_details(self,link):
        page = self.fetch_page(link)
        html = self.fromstring(page) 
        car_body = self.locate(html,'div.postWrapper')[0]
        car_body = self.tostring(car_body)
        car_body = self.clean(car_body)
        return car_body

    def run(self):
        self.get_list_item()

if __name__ == '__main__':
    car = Caranddrive('http://blog.caranddriver.com')
    car.run()


                            
