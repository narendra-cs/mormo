#!/usr/bin/python

from pymongo import MongoClient
import datetime,os,urllib

MONGODB_USER = urllib.quote_plus('mormow')
MONGODB_PASSWD = urllib.quote_plus('passwd#123@QW!')
MONGODB_HOST = '10.208.35.113'
MONGODB_PORT = '27017'
MONGODB_NAME = 'commandlogs'
collection_name = 'logs'

log_file = '/var/log/mlog'


MONGODB_URI = 'mongodb://%s:%s@%s:%s/%s?authSource=%s' % (MONGODB_USER,MONGODB_PASSWD,MONGODB_HOST,MONGODB_PORT,MONGODB_NAME,MONGODB_NAME)

db = MongoClient(MONGODB_URI).get_database(MONGODB_NAME)

collection = db[collection_name]

posts=[]

try:
	with open(log_file,'r') as logs:
		for line in logs:
			values=line.strip('\n').strip().split('\t')
			d=values[0].split('-')
			timestamp=datetime.datetime.strptime('-'.join([d[0][-2:],d[1],d[2]])+' '+values[1],'%y-%m-%d %H:%M:%S')
			tmp={"timestamp":timestamp,"user":values[2],"identity":values[3],"host":values[4],"cmd":values[5]}
			posts.append(tmp)
except IOError:
			print("Error: log file not found")

# insert in bulk

result=collection.insert_many(posts).inserted_ids
