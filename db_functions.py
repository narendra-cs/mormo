# -*- coding: utf-8 -*-
'''
This file having utilit function Regarding, connection to databse i.e. MongoDB in our case.
'''

__author__ = "Narendra Singh"


def mongoConnection():
    '''
    :return: object of MongoClient

    MongoDB Connection to server and database, define in mormo.conf .
    '''

    # Import required modules with exception handling. so if module is not available it will print error.
    # else load configuration from mormo.conf file.
    try:
        '''
        Import module thorugh __import__() so it would not be available as 
        one of the function of this file when we import this file.
        '''
        config = __import__('config')
        pymongo  = __import__('pymongo')
    except ImportError as e:
        print(e.__class__.__name__ + ": " + str(e))
    else:
        _cfg = config.confLoader()

    # import "quote" function from urllib in python-2, if exception, import python-3 version of "quote"
    try:
        from urllib import quote
    except ImportError:
        from urllib.parse import quote

    # Getting MongoDB conf and return MongoClient object to specified server and database.
    if 'MONGODB' in _cfg.keys():
        cnf  = _cfg['MONGODB']
        uri  = 'mongodb://{user}:{pwd}@{host}:{port}/{db}?authSource={db}'.format(user=quote(cnf['USER']),pwd=quote(cnf['PASSWD']),host=cnf['HOST'],port=cnf['PORT'],db=cnf['DBNAME'])
        return pymongo.MongoClient(uri).get_database(cnf['DBNAME'])
    else:
        print("mongodb configurations are not in mormo.conf file.")
        return
