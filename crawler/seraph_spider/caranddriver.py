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
import requests,lxml.html
from lxml.html.clean import Cleaner
import logging
import logging.config

logging.config.fileConfig('crawler/seraph_spider/logging.conf')
logger = logging.getLogger('caranddriver')

def spiderboy():
    return