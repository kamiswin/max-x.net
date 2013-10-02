# -*- encoding: utf-8 -*-
__author__ = 'seraph'
import lxml.html,requests,sys

reload(sys)
sys.setdefaultencoding('utf-8')
page = requests.get('http://drive.chinaluxus.com/Chinaluxus/20130925/287145.html')
html = lxml.html.fromstring(page.content)

base_url = '/'.join(page.url.split('/')[:-1])+'/'


while len(html.cssselect('.next')) > 0 and len(html.cssselect('.nextBtn')) == 0:
    nextpage = requests.get(base_url + html.cssselect('.next')[0].get('href'))
    print nextpage.url
    nexthtml = lxml.html.fromstring(nextpage.content)
    print nexthtml.cssselect('.text')[-1]
    print lxml.html.tostring(nexthtml.cssselect('.text')[-1],encoding='utf-8')
    html = nexthtml