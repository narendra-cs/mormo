# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def error_404(request):
    return render(request,'error/404.html',{})

def error_500(request):
    return render(request,'error/500.html',{})