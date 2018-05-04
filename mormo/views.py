# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def index(request):
	return render(request,'index.html',{})

def contact(request):
	return render(request,'contact.html',{})

def error_404(request):
    return render(request,'error/404.html',{})

def error_500(request):
    return render(request,'error/500.html',{})