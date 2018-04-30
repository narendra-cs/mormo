#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():

    # import required modules
    try:
        datetime    = __import__('datetime')
        db_functions= __import__('db_functions')
    except ImportError as e:
        print(e.__class__.__name__ + ": " + str(e))

    # constant parameters, should not be change
    collection_name = 'logs'
    log_file        = '/var/log/mlog'

    # collection object of our collection in MongoDB
    collection      = db_functions.mongoConnection()[collection_name]
    
    # generating dictionary object to dump data into MongoDB
    posts = []
    try:
        with open(log_file,'r') as logs:
            for line in logs:
                values=line.strip('\n').strip().split('\t')
                d=values[0].split('-')
                timestamp=datetime.datetime.strptime('-'.join([d[0][-2:],d[1],d[2]])+' '+values[1],'%y-%m-%d %H:%M:%S')
                posts.append({"timestamp":timestamp,"user":values[2],"identity":values[3],"host":values[4],"cmd":values[5]})
    except IOError:
        print("Error: log file not found")

    # insert data into MongoDB
    collection.insert_many(posts)


if __name__ == '__main__':
    main()