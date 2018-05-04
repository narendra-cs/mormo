# -*- coding: utf-8 -*-
from django.conf.urls import include,handler404,handler500,re_path
from django.contrib import admin
from . import views

app_name = 'mormo'

urlpatterns = [
    # /
    re_path(r'^$',views.index,name='index'),
    # /contact/
    re_path(r'^contact/$',views.contact,name='contact'),
    # /admin/
    re_path(r'^admin/', admin.site.urls),
    # /logs/
    re_path(r'^logs/',include('cmdMonitor.urls',namespace='cmdMonitor')),
    # /accounts/
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
]

handler404=views.error_404
handler500=views.error_500
