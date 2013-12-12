#encoding:utf-8
# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import RequestContext
from django.shortcuts import render_to_response as render
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.utils import simplejson
#from django.template import loader
from forms import *
from models import UserProfile

@csrf_protect
def register(request):
    if request.method == 'POST':
        rf = RegisterForm(request.POST)

        if rf.is_valid():
            data = rf.clean()
        else:
            # 数据不合法
            return HttpResponse(simplejson.dumps({
                        'status':'type worong',
                        # 'content':'content'
                        
                    }, ensure_ascii=False),content_type="application/json")

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            pass
        else:
            # 用户名已经存在
            return HttpResponse(simplejson.dumps({
                        'status':'already exist',
                        # 'username':'',
                    }, ensure_ascii=False), content_type="application/json")

        new_user = User.objects.create_user(username=data['username'],email=data['username'],password=data['password'])
        new_user.save()
        new_profile = UserProfile(user=new_user,screen_name=data['screen_name'])

        new_profile.save()

        return HttpResponse(simplejson.dumps({
                        'status':'success',
                        # 'username':'',
                    }, ensure_ascii=False), content_type="application/json")

    else:
        rf = RegisterForm()
        # 不是post请求
    return HttpResponse(simplejson.dumps({
            'status':'not post',
            # 'username':'',
        }, ensure_ascii=False))


@csrf_protect
def login(request):
    if request.method == 'POST':
        lf = LoginForm(request.POST)
        if lf.is_valid():
            data = lf.clean()

            try:
                user = User.objects.get(username=data['username'])
            except User.DoesNotExist:
                # messages.error(request,"这个email还没注册过，果断注册")
                # return render('login.html',locals(),context_instance=RequestContext(request))
                return HttpResponse(simplejson.dumps({
                        'status':'not exist',
                        'username':'',
                    }, ensure_ascii=False), content_type="application/json")

            user = authenticate(username=data['username'],password=data['password'])
            if user is not None:
                auth_login(request,user)
                return_user = User.objects.get(username=data['username'])
                # return HttpResponseRedirect('/')
                # screen_name = return_user.screen_name
                return HttpResponse(simplejson.dumps({
                        'status':'already',
                        'username':return_user.username,
                    }, ensure_ascii=False),content_type="application/json")
            else:
                messages.error(request,'密码错误')

        # return render('login.html',locals(),context_instance=RequestContext(request))
        return HttpResponse(simplejson.dumps({
                        'status':'type worong',
                        'content':'content'
                        
                    }, ensure_ascii=False),content_type="application/json")

    lf = LoginForm()
    # return render('login.html',{'lf':lf},context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps({
            'status':'not post',
            'username':'',
        }, ensure_ascii=False))


def logout(request):
    auth_logout(request)
    request.session['access_token'] = ''
    request.session['request_token'] = ''
    return HttpResponseRedirect('/')