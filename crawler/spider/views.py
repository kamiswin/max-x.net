# -*- encoding:utf-8 -*-
# Create your views here.
from django.http import Http404
from django.http import HttpResponse
from django.template import Context,loader
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from spider.models import Car
import logging
#from django.db.models import Q

logger = logging.getLogger(__name__)

def index(request):
    car_list = Car.objects.all()
    template = loader.get_template('car_list.html')
    context = Context(
        {'car_list':car_list,}

    )
    return HttpResponse(template.render(context))

def detail(request, car_id):
    try:
        car = Car.objects.get(pk=car_id)
        car_rencent = Car.objects.all().order_by('-car_time')[:10]
        template = loader.get_template('car_detail.html')
        context = Context({
            'car':car,
            'car_rencent':car_rencent,
        })
    except Car.DoesNotExist:
        raise Http404

    return HttpResponse(template.render(context))


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
    })
    return HttpResponse(template.render(context))
