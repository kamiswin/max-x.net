# -*- coding: utf-8 -*-
__author__ = 'seraph'
import requests


# url time
chinaluxus_url = 'http://drive.chinaluxus.com/Cul/'


import lxml.html

page = requests.get(chinaluxus_url)

html = lxml.html.fromstring(page.content)
for i in html.cssselect('.listDetail'):
    #text_list = []
    print 'title',i.cssselect('.fb14d')[0].text_content()
    print 'body',i.cssselect('.spanText')[0].text_content()

    link = i.cssselect('.fb14d a')[0].get('href')
    print 'link',i.cssselect('.fb14d a')[0].get('href')
    print 'icon',i.cssselect('.img img')[0].get('src')

    innerpage = requests.get(link)
    #print innerpage.content
    innerhtml = lxml.html.fromstring(innerpage.content)

    boo = innerhtml.cssselect('.text')[-1]
    if boo.text_content() == u'支持度':
        print '==================================================='
        body = innerhtml.cssselect('.explainPic')[0]
        fin_body = lxml.html.tostring(body,encoding='utf-8')
        print fin_body
    #print boo.text_content()
    print lxml.html.tostring(innerhtml.cssselect('.text')[-1],encoding='utf-8')
