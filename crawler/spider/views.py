# -*- encoding:utf-8 -*-
# Create your views here.
from django.http import Http404
#from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
#from django.template import Context,loader
#from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
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
    #username = request.session.get('username','')


    query = None
    site = None
    #logger.info('james')
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
    # paginator = Paginator(car_list,10)
    # try:
    #     page = request.GET.get('page','1')
    # except:
    #     page = 1

    # try:
    #     car = paginator.page(page)
    # except PageNotAnInteger:
    #     car = paginator.page(1)
    # except EmptyPage:
    #     car = paginator.page(paginator.num_pages)



    return render_to_response('car_list.html',{
            'query':query,
            'site':site,
            'car_list':car_list,
            'car_rencent':car_rencent,
            #'car':car,
        },context_instance=RequestContext(request))


def details_show_comment(request, id=''):
    details = Car.objects.get(id=id)
    return render_to_response('details_comments_show.html', {"details": details})


#def ajax_list(request):



