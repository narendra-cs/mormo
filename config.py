# -*- coding: utf-8 -*-
'''
This file having function to load configuration from mormo.conf file i.e. default configuration file
for the host system on which we have to capture the commands.
'''

__author__ = "Narendra Singh"


def confLoader(filepath='mormo.conf'):
    '''
    :param filepath: configuration file name
    :return: configuration as dictionary

    Load mormo configuration and return it.
    '''

    # import yaml module to load configuration from yaml file with exception handling.
    # so if module is not available it will print error.
    try:
        '''
        Import module thorugh __import__() so it would not be available as 
        one of the function of this file when we import this file.
        '''
        yaml    = __import__('yaml')
    except ImportError as e:
        print(e.__class__.__name__ + ": " + str(e))

    # Load mormo configuration from *.conf file. also handle excpetion if file is not there and in note proper YAML format.
    try:
        with open(filepath,"r") as fd0:
            data = yaml.load(fd0)
    except FileNotFoundError as e:
        print("Error {1}: {2} {0}".format(filepath,*e.args))
    except yaml.YAMLError as e:
        print("Error: configuration file is not in proper YAML format.")
        print(e)
    else:
        return data
