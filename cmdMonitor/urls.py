# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import re_path
from . import views

app_name = 'cmdMonitor'

urlpatterns = [
	re_path(r'^$',views.index,name='index'),
	re_path(r'^search/$',views.search,name='search'),
	re_path(r'^download/(?P<filename>\w+\.\w+)/$',views.download,name='download'),
]
