import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'this-place-we-should-put-some-random-key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'test_db_repository')


config = {
    'dev': DevelopmentConfig,
    'default': DevelopmentConfig,
    'test': TestConfig
}
