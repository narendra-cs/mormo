#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Read logs from mlog file,make them in proper format ( json, dictionary in python ) and dump into collection of MongoDB database.
'''

__author__ = "Narendra Singh"


def main():
    '''
    Import require module with exception handling. so if module is not available it will print error.
    '''
    try:
        '''
        Import module thorugh __import__() so it would not be available as 
        one of the function of this file when we import this file.
        '''
        datetime    = __import__('datetime')
        db_functions= __import__('db_functions')
    except ImportError as e:
        print(e.__class__.__name__ + ": " + str(e))

    # Constant parameters, should not be change
    collection_name = 'logs'
    log_file        = '/var/log/mlog'

    # Collection object of logs collection in MongoDB
    collection      = db_functions.mongoConnection()[collection_name]
    
    # Generating dictionary object to dump data into MongoDB
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

    # Insert data into MongoDB
    collection.insert_many(posts)

# Run main function if script is execute directly not through import.
if __name__ == '__main__':
    main()