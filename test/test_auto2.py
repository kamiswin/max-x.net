# -*- encoding:utf-8 -*-
__author__ = 'seraph'
import lxml.html, requests, re

page = requests.get('http://www.autohome.com.cn/news/201310/632977.html')
html = lxml.html.fromstring(page.content.decode('gbk','ignore'))
print '相关阅读'.decode('utf-8') in page.content.decode('gbk')
article = html.cssselect('#articleContent')[0]
arttext = lxml.html.tostring(article)
print isinstance(arttext,basestring)

print '相关阅读'.decode('utf-8') in arttext

arttext2 = lxml.html.fromstring(arttext)
arttext3 = lxml.html.tostring(arttext2,encoding='gbk')

print 3333 ,arttext3


r = re.compile(r'相关阅读.*')
fi = r.findall(arttext)

for i in fi:
    print 44444,i

