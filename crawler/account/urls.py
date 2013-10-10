#encoding:utf-8
__author__ = 'seraph'
from django.conf.urls import patterns, url
from account import views

urlpatterns = patterns('',
    url(r'regist/$',views.register,name='regist'),
    url(r'login/$',views.login,name='login'),
    url(r'logout/$',views.logout,name='logout'),
)


