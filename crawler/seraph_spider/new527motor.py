#!/usr/bin/env python
#              encoding:utf-8
import         re
from           gevent import monkey
monkey.patch_all()
from base import BaseCraw
import lxml.html
from spider.models import Car


class Newmotor(BaseCraw):

    # url = 'http://www.527motor.com/portal.php'
    def __init__(self,url):
        BaseCraw.__init__(self,url)


    def get_category(self):
        cate_list = []
        page = self.fetch_page(self._url)
        html = self.fromstring(page)
        categories = html.cssselect('li[id^="mn"]')
        cate_list.append(categories[1])
        cate_list.append(categories[2])
        cate_list.append(categories[4])
        cate_list.append(categories[6])
        cate_list.append(categories[7])
        return cate_list



    def get_list(self):
        cate_link = []
        nodes_list = []
        cate_list = self.get_category()
        for cate in cate_list:
            cate_link.append(cate.cssselect('a')[0].get('href'))
            print cate.cssselect('a')[0].get('href')

        for cate_ad in cate_link:
            print cate_ad
            page = self.fetch_page(cate_ad)
            html = self.fromstring(page)
            nodes = self.locate(html,'.bbda')
            nodes_list.extend(nodes)

        return nodes_list


    def get_list_info(self):
        nodes_list = self.get_list()
        for node in nodes_list:
            car_link = self._url.rsplit('/',1)[0] + '/' + node.cssselect('.xs2 a')[0].get('href')
            print 'carlink ',car_link
            try:
                Car.objects.get(car_link=car_link)
                print 'already have ',car_link
                pass
            except Exception,e:
                print node.cssselect('.xs2 a')[0].text_content()
                car_title = node.cssselect('.xs2 a')[0].text_content().encode('utf-8')
                car_icon = self._url.rsplit('/',1)[0] + '/' + node.cssselect('.atc img')[0].get('src')
                car_des = node.cssselect('.xs2.cl')[0].text_content().encode('utf-8')

                innerpage = self.js_fetch(car_link)
                innerhtml = self.findby('body')
                self.kill_dr()
                innerhtml = lxml.html.fromstring(innerhtml)

                try:
                    writer = self.tostring(innerhtml.cssselect('.xg1')[0])
                except:
                    writer = self.tostring(innerhtml.cssselect('.xg1')[0])

                mid_body = self.tostring(innerhtml.cssselect('#article_content')[0])

                pattern = re.compile(
                    r'(?:src|href)="([^http].*?[\.jpg])"', re.VERBOSE)

                test = pattern.findall(mid_body)
                test = list(set(test))

                for i in test:
                    mid_body = mid_body.replace(i, self._url.rsplit('/',1)[0] + '/' + i)

                car_body = writer + mid_body

                ca = Car(car_title=car_title,
                         car_des=car_des,
                         car_link=car_link,
                         car_body=car_body,
                         car_icon=car_icon,
                         car_source="527motor",
                         car_cate='motorbike')

                ca.save()
                print 'done'

    def run(self):
        self.get_list_info()

if __name__ == '__main__':
    motor = Newmotor('http://www.527motor.com/portal.php')
    motor.run()









