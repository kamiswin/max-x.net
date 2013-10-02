__author__ = 'seraph'
import lxml.html
import requests

page = requests.get('http://drive.chinaluxus.com/Lif/20130923/287005.html')

html = lxml.html.fromstring(page.content)

print lxml.html.tostring(html.cssselect('.explainPic')[0],encoding='utf-8')

last_url = ''

while len(html.cssselect('.nextBtn')) > 0:
    print str(html.cssselect('.nextBtn')[0].get('href'))
    print str(last_url)
    if str(html.cssselect('.nextBtn')[0].get('href')) != str(last_url):
        nextpage = requests.get(html.cssselect('.nextBtn')[0].get('href'))
        nexthtml = lxml.html.fromstring(nextpage.content)
        last_url = nextpage.url
        print lxml.html.tostring(nexthtml.cssselect('.explainPic')[0],encoding='utf-8')
        html = nexthtml
    else:
        break

