# -*- encoding:utf-8 -*-
__author__ = 'seraph'
import lxml.html,requests


autohome_url = 'http://www.autohome.com.cn/list/c71-1.html'

page = requests.get(autohome_url)


print 'ATitle' in page
html = lxml.html.fromstring(page.content.decode('gb2312','ignore'))
for i in html.cssselect('#ATitle'):

    print 'car_title',i.text_content()
    print 'car_icon','seraph'
    print 'car_des',i.text_content()
    print 'car_link',i.get('href')
    innerpage = requests.get(i.get('href'))
    innerhtml = lxml.html.fromstring(innerpage.content.decode('gbk','ignore'))
    print 'car_body',innerhtml.cssselect('.article-content')[0].text_content()

