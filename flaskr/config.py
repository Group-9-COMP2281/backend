class Config(object):
    DEBUG = False
    DEVELOPMENT = False

    # todo, load from file?
    MYSQL_DATABASE_USER = 'root'

    #Enter password here
    MYSQL_DATABASE_PASSWORD = ''
    
    MYSQL_DATABASE_DB = 'engagement-db'
    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_CHARSET = 'utf8mb4'
    
    # Change this if a different port number is used
    MYSQL_DATABASE_PORT = 3306


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = 'root'
    MYSQL_DATABASE_DB = 'engagement-db'
    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_CHARSET = 'utf8mb4'


config = {
    'default': Config,
    'config': Config,
    'dev': DevConfig
}

get_config = lambda key: config.get(key or 'default', config.get('default'))
