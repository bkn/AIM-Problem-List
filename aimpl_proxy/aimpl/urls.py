from django.conf.urls.defaults import *

from aimpl_proxy.aimpl.views import index, pl_detail, sec_detail, remark_detail, \
remark_queue, remark_moderate

urlpatterns = patterns('',
    (r'^$', index),
    (r'^remarkqueue$', remark_queue),
    (r'^remarkqueue/$', remark_queue),
    (r'^remarkqueue/(?P<plname>[\w-]+)$', remark_moderate),
    (r'^remarkqueue/(?P<plname>[\w-]+)/$', remark_moderate),
    (r'^(?P<plname>[\w-]+)$', pl_detail),
    (r'^(?P<plname>[\w-]+)/$', pl_detail),
    (r'^(?P<plname>[\w-]+)/v(?P<version>\d{0,3}\.\d{0,2})$', pl_detail),
    (r'^(?P<plname>[\w-]+)/v(?P<version>\d{1,3}\.\d{1,2})/$', pl_detail),
    
    
    (r'^(?P<plname>[\w-]+)/(?P<secnum>\d+)$', sec_detail),
    (r'^(?P<plname>[\w-]+)/(?P<secnum>\d+)/$', sec_detail),
    (r'^(?P<plname>[\w-]+)/v(?P<version>\d{1,3}\.\d{1,2})/(?P<secnum>\d+)$', sec_detail),
    (r'^(?P<plname>[\w-]+)/v(?P<version>\d{1,3}\.\d{1,2})/(?P<secnum>\d+)/$', sec_detail),
    (r'^(?P<plname>[\w-]+)/(?P<secnum>\d+)\.(?P<blocknum>\d+)$', sec_detail),
    (r'^(?P<plname>[\w-]+)/(?P<secnum>\d+)\.(?P<blocknum>\d+)/$', sec_detail),
    (r'^(?P<plname>[\w-]+)/v(?P<version>\d{1,3}\.\d{1,2})/(?P<secnum>\d+)\.(?P<blocknum>\d+)$', sec_detail),
    (r'^(?P<plname>[\w-]+)/v(?P<version>\d{1,3}\.\d{1,2})/(?P<secnum>\d+)\.(?P<blocknum>\d+)/$', sec_detail),
    
    (r'^(?P<plname>[\w-]+)/(?P<secnum>\d+)\.(?P<blocknum>\d+)/remark/(?P<remarknum>\d+)$', remark_detail),
    (r'^(?P<plname>[\w-]+)/(?P<secnum>\d+)\.(?P<blocknum>\d+)/remark/(?P<remarknum>\d+)/$', remark_detail),
)
