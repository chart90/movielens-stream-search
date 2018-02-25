import configparser

config = configparser.RawConfigParser()
config.read('config/config.ini')

USERNAME = config.get('LOGIN', 'USERNAME')
PASSWORD = config.get('LOGIN', 'PASSWORD')
