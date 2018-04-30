# -*- coding: utf-8 -*-

def mongoConnection():
    """ MongoDB Connection to server and database define in mormo.conf """
    
    # import required modules
    try:
        confload = __import__('config')
        pymongo  = __import__('pymongo')
        urllib   = __import__('urllib')
    except ImportError as e:
        print(e.__class__.__name__ + ": " + str(e))

    # getting MongoDB conf from mormo.confg file
    cnf  = confload.confLoader()
    user = urllib.quote_plus(cnf['MONGODB']['USER'])
    pwd  = urllib.quote_plus(cnf['MONGODB']['PASSWD'])
    host = cnf['MONGODB']['HOST']
    port = cnf['MONGODB']['PORT']
    db   = cnf['MONGODB']['DBNAME']
    uri  = 'mongodb://%s:%s@%s:%s/%s?authSource=%s' % (user,pwd,host,port,db,db)
    return pymongo.MongoClient(uri).get_database(db)
