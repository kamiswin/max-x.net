__author__ = 'max'
import lxml.html,requests

page = requests.get('http://www.skype.com/go/store.buy.skypecredit')

print page.text