#!/usr/bin/env python
# encoding:utf-8
import os
import sys
selfpath = os.path.split(os.path.realpath(__file__))[0]
PATH = os.path.abspath(os.path.join(selfpath,'..'))
sys.path.append(PATH)
from crawler import settings          #your project settings file
from django.core.management import setup_environ     #environment setup function
setup_environ(settings)
from spider.models import Car
import lxml.html

old_icon = 'http://x.autoimg.cn/news/index/img/20110801/logo_new.png'


def get_content_icon():
    car_list = Car.objects.filter(car_source='autohome',car_icon=old_icon)
    return car_list


def get_content_des():
    car_list = Car.objects.filter(car_source='autohome')
    return car_list


def autohome_fix_icon():
    car_list = get_content_icon()
    for car in car_list:
        new_car_icon = old_icon
        html = lxml.html.fromstring(car.car_body)
        car_icon_list = html.cssselect('img')
        if len(car_icon_list) > 0:
            new_car_icon = car_icon_list[0].get('src')
        car.car_icon = new_car_icon
        print car.car_title
        car.save()



def autohome_fix_des():
    car_list = get_content_des()
    print len(car_list)
    for car in car_list:
        new_car_des = ' '
        html = lxml.html.fromstring(car.car_body)
        car_des_list = html.cssselect('p:empty')
        if len(car_des_list) > 0:
            new_car_des = car_des_list[0].text
        car.car_des = new_car_des
        print car.car_title
        car.save()




if __name__=="__main__":
    autohome_fix_icon()
    # autohome_fix_des()