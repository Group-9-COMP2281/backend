class Config(object):
    DEBUG = False
    DEVELOPMENT = False

    # todo, load from file?
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = ''
    MYSQL_DATABASE_DB = 'engagement-db'
    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_CHARSET = 'utf8mb4'


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
