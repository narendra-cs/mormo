# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Logs
from datetime import datetime
import pandas as pd
import os

# Global variables
logs=''
download_q={}


# index view
@login_required
def index(request):
	logs=Logs.objects.all()
	return render(request,'cmdMonitor/index.html',{'all_logs':logs})

# generate file for Download
def generateFile(logs,filename='logs.xlsx'):
	timestamp_data =  []
	users =  []
	identity =  []
	host =  []
	cmd = []

	for log in logs:
		timestamp_data.append(log.timestamp)
		users.append(log.user)
		identity.append(log.identity)
		host.append(log.host)
		cmd.append(log.cmd)

	log_dict={'timestamp':timestamp_data,'user':users,'identity':identity,'host':host,'command':cmd}
	log_df=pd.DataFrame.from_dict(log_dict,orient='index')
	log_df=log_df.transpose()

	file_path=os.path.join(settings.STATIC_ROOT,filename)
	if os.path.isfile(file_path):
		os.remove(file_path)

	if '.xlsx' == os.path.splitext(filename)[-1]:
		log_df.to_excel(file_path,sheet_name='logs',index=False)
	elif '.csv' == os.path.splitext(filename)[-1]:
		log_df.to_csv(file_path,index=False)
	elif '.json' == os.path.splitext(filename)[-1]:
		log_df.to_json(file_path,orient="records",date_format='iso')
	return file_path

@login_required
def search(request):
	global download_q
	querry={}
	regex=''
	from_req = request.POST['from']
	to = request.POST['to']
	user = request.POST['user']
	identity = request.POST['identity']
	host = request.POST['host']
	cmd = request.POST['cmd']
	cmd_regex = request.POST['cmd_regex'].lower()

	if len(from_req)>1:
		querry['timestamp__gte'] = datetime.strptime(from_req,'%m/%d/%Y %I:%M %p')
	if len(to)>1:
		querry['timestamp__lte'] = datetime.strptime(to,'%m/%d/%Y %I:%M %p')
	if len(user)>1:
		querry['user'] = user
	if len(identity)>1:
		querry['identity'] = identity
	if len(host)>1:
		querry['host__icontains'] = host
	if len(cmd)>1:
		if len(cmd_regex)>1:
			querry['cmd__i'+cmd_regex] = cmd
			regex=cmd_regex
		else:
			querry['cmd'] = cmd
	download_q=querry
	logs=Logs.objects.filter(**querry).order_by('-timestamp')
	if 'timestamp__gte' in querry.keys():
		querry['timestamp__gte']=querry['timestamp__gte'].strftime('%m/%d/%Y %I:%M %p')
	if 'timestamp__lte' in querry.keys():
		querry['timestamp__lte']=querry['timestamp__lte'].strftime('%m/%d/%Y %I:%M %p')
	context={'all_logs':logs,'download_file':'True','querry':querry,'regex':regex}
	return render(request,'cmdMonitor/index.html',context)

@login_required
def download(request,filename):
	logs=Logs.objects.filter(**download_q).order_by('-timestamp')
	path_to_file=generateFile(logs,filename)
	with open(path_to_file,'rb') as f:
		response = HttpResponse(f.read(),content_type='application/force-download')
		response['Content-Disposition'] = 'attachment; filename=%s' % (filename)
		response['X-Sendfile'] = path_to_file
	return response