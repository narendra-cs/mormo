# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url,include
from . import views

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^search/$',views.search,name='search'),
	url(r'^download/(?P<filename>\w+\.\w+)/$',views.download,name='download'),
]
