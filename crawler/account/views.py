#encoding:utf-8
# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import RequestContext
from django.shortcuts import render_to_response as render
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.template import loader
from forms import *
from models import UserProfile

@csrf_protect
def register(request):
    rf = RegisterForm()
    return render('regist.html',{'rf':rf},context_instance=RequestContext(request))


@csrf_protect
def login(request):
    lf = LoginForm()
    return render('login.html',{'lf':lf},context_instance=RequestContext(request))


def logout(request):
    return HttpResponseRedirect('/')