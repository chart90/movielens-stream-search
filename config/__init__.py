import configparser

config = configparser.RawConfigParser()
config.read('config/config.ini')

USERNAME = config.get('MOVIELENS', 'USERNAME')
PASSWORD = config.get('MOVIELENS', 'PASSWORD')

COUNTRY = config.get('JUSTWATCH', 'COUNTRY')
