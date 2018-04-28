# encoding=utf-8
'''
Configuration file(demo_config.ini) parser
'''
import os

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

api_config = ConfigParser.ConfigParser()

api_config.read(os.path.join(os.path.dirname(__file__), 'config.ini').replace('\\', '/'))


APPCODE =api_config.get('datasource','APPCODE')
HEADERS={'Authorization': APPCODE }