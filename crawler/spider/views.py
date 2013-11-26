# -*- encoding:utf-8 -*-
# Create your views here.
from django.http import Http404
from django.shortcuts import render_to_response, RequestContext
from models import Car
from django.views.decorators.csrf import csrf_protect
import logging

logger = logging.getLogger(__name__)


@csrf_protect
def detail(request, car_id):
    #username = request.session.get('username','')
    try:
        car = Car.objects.get(pk=car_id)
        car_rencent = Car.objects.all().order_by('-car_time')[:10]

    except Car.DoesNotExist:
        raise Http404

    return render_to_response('car_detail.html',locals(),context_instance=RequestContext(request))


@csrf_protect
def listing(request,car_cate=None):
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

    car_list = car_list[:10]

    car_rencent = Car.objects.all().order_by('-car_time')[:10]


    return render_to_response('car_list.html',{
            'query':query,
            'site':site,
            'car_list':car_list,
            'car_rencent':car_rencent,
        },context_instance=RequestContext(request))


#@csrf_protect
def listing_ajax(request,car_cate=None):
    nums = 10
    query = None
    site = None
    if 'site' in request.GET:
        site = request.GET['site']

    if 'query' in request.GET:
        query = request.GET['query']

    if 'nums' in request.GET:
        nums = request.GET['nums']
        nums = int(nums)
    if 'category' in request.GET:
        car_cate = request.GET['category']

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

    car_list = car_list[nums:nums+10]

    car_rencent = Car.objects.all().order_by('-car_time')[:10]


    return render_to_response('car_list_ajax.html',{
            'query':query,
            'site':site,
            'car_list':car_list,
            'car_rencent':car_rencent,
        })




def details_show_comment(request, id=''):
    details = Car.objects.get(id=id)
    return render_to_response('details_comments_show.html', {"details": details})


#def ajax_list(request):



