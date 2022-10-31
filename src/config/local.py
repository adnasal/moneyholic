from src.config.common import *  # noqa

# Testing
INSTALLED_APPS += ('django_nose',)  # noqa
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['-s', '--nologcapture', '--with-fixture-bundling', '--verbosity=5', '--with-coverage',
             '--cover-package=newscraper', '--cover-html']


