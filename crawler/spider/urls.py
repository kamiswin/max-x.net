__author__ = 'seraph'
from django.conf.urls import patterns, url
from spider import views

urlpatterns = patterns('',
    url(r'^$',views.listing, name='index'),
    url(r'^(?P<car_cate>[a-z]+)/$',views.listing, name='index'),
    url(r'^(?P<car_id>\d+)/$',views.detail,name='detail')
)
