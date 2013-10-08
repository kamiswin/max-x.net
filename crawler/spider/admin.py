__author__ = 'seraph'
from django.contrib import admin
from spider.models import Car
from spider.models import User

#admin.site.register(Car)

class CarAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None,{'fields':['car_title']}),
        ('categroy',{'fields':['car_source','car_cate'],'classes':['collapse']}),
        ('information',{'fields':['car_des','car_body','car_link','car_icon']})
    ]
    list_display = ('car_title','car_time','car_cate','car_source')


    list_filter = ['car_cate',
                   'car_time',
                   'car_source',
                   ]

    search_fields = ['car_title']

    date_hierarchy = 'car_time'

    list_per_page = 15



class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password','signtime')

admin.site.register(Car,CarAdmin)
admin.site.register(User,UserAdmin)