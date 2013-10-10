# -*- encoding:utf-8 -*-
# Create your views here.
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.template import Context,loader
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from models import Car
#from spider.forms import UserForm
from django.views.decorators.csrf import csrf_protect
import logging
#from django.db.models import Q

logger = logging.getLogger(__name__)

def index(request):
    car_list = Car.objects.all()
    template = loader.get_template('car_list.html')
    context = RequestContext(
        {'car_list':car_list,}

    )
    return HttpResponse(template.render(context))


@csrf_protect
def detail(request, car_id):
    #username = request.session.get('username','')
    try:
        car = Car.objects.get(pk=car_id)
        car_rencent = Car.objects.all().order_by('-car_time')[:10]

    except Car.DoesNotExist:
        raise Http404

    return render_to_response("car_detail.html",{
        'car':car,
        'car_rencent':car_rencent,
        'username':username,
        },context_instance=RequestContext(request))


@csrf_protect
def listing(request,car_cate=None):
    username = request.session.get('username','')

    query = None
    site = None
    if 'site' in request.GET:
        site = request.GET['site']
    if 'query' in request.GET:
        query = request.GET['query']
    if site:
        if car_cate:
            car_list = Car.objects.filter(car_source=site,car_cate=car_cate).order_by('-car_time')
        else:
            car_list = Car.objects.filter(car_source=site).order_by('-car_time')
    elif query:
        car_list = Car.objects.filter(car_title__contains=query).order_by('-car_time')
    elif car_cate:
        car_list = Car.objects.filter(car_cate=car_cate).order_by('-car_time')
    else:
        car_list = Car.objects.all().order_by('-car_time')

    car_rencent = Car.objects.all().order_by('-car_time')[:10]
    #car_list = Car.objects.filter(car_cate='car')
    paginator = Paginator(car_list,10)

    page = request.GET.get('page')

    try:
        car = paginator.page(page)
    except PageNotAnInteger:
        car = paginator.page(1)
    except EmptyPage:
        car = paginator.page(paginator.num_pages)
    template = loader.get_template('car_list.html')
    context = Context({
        'car_list':car,
        'car_rencent':car_rencent,
        #'username':username,
        'site':site,
        'query':query,
        })
    return HttpResponse(template.render(context))


#@csrf_protect
#def regist(request):
#    if request.method == 'POST':
#        uf = UserForm(request.POST)
#        if uf.is_valid():
#            username = uf.cleaned_data['username']
#            password = uf.cleaned_data['password']
#            User.objects.create(username = username,password = password)
#            return HttpResponseRedirect('/login/')
#    else:
#        uf = UserForm()
#    return render_to_response('regist.html',{'uf':uf},context_instance=RequestContext(request))
#
#
#@csrf_protect
#def login(request):
#    if request.method == 'POST':
#        uf = UserForm(request.POST)
#        if uf.is_valid():
#            username = uf.cleaned_data['username']
#            password = uf.cleaned_data['password']
#            user = User.objects.filter(username__exact = username, password__exact = password)
#            if user:
#                request.session['username'] = username
#                return HttpResponseRedirect('/')
#            else:
#                return HttpResponseRedirect('/login/')
#    else:
#        uf = UserForm()
#    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))
#
#@csrf_protect
#def logout(request):
#    session = request.session.get('username', False)
#    if session:
#        del request.session['username']
#        return render_to_response('logout.html',{'username':session},context_instance=RequestContext(request))
#    else:
#        #return HttpResponse('please login!')
#        return HttpResponseRedirect('/')