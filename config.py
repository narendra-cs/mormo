# -*- coding: utf-8 -*-

def confLoader():
    """ Load mormo configuration  """

    # import yaml module to load configuration from yaml file
    try:
        yaml    = __import__('yaml')
    except ImportError as e:
        print(e.__class__.__name__ + ": " + str(e))
    
    # name of yaml file
    filepath    = 'mormo.conf'

    # Loading mormo configuration from *.conf file
    try:
        with open(filepath,"r") as fd0:
            data = yaml.load(fd0)
    except FileNotFoundError as e:
        print("Error {1}: {2} {0}".format(filepath,*e.args))
    except yaml.YAMLError as e:
        print("Error:")
        print(e)
    else:
        return data
