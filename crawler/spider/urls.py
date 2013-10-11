__author__ = 'seraph'
from django.conf.urls import patterns, url
from spider import views

urlpatterns = patterns('',
    url(r'^$',views.listing, name='index'),
    #url(r'regist/$',views.regist,name='regist'),
    #url(r'login/$',views.login,name='login'),
    #url(r'logout/$',views.logout,name='logout'),
    url(r'^(?P<car_cate>[a-z]+)/$',views.listing, name='cate'),
    url(r'^(?P<car_id>\d+)/$',views.detail,name='detail'),
    url(r'^blog/(?P<id>\d+)/commentshow/$', views.details_show_comment, name='showcomment'),

)
