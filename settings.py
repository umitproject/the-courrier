#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
## Author: Adriano Marques <adriano@umitproject.org>
##
## Copyright (C) 2012 S2S Network Consultoria e Tecnologia da Informacao LTDA
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os


# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native',
                        'HIGH_REPLICATION': True}
AUTOLOAD_SITECONF = 'indexes'

SECRET_KEY = 'luycouistdf8atyoweiurhql4rhnoaetf89asy9uhryugekjvf32234567890'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
CACHE_MIDDLEWARE_SECONDS = 30

ENVIRONMENT = os.environ.get('SERVER_SOFTWARE', '')
GAE = True
PRODUCTION = True
TEST = False

if ENVIRONMENT == '':
    GAE = False
elif ENVIRONMENT.startswith('Development'):
    PRODUCTION = False
elif ENVIRONMENT.startswith('GAETest'):
    TEST = True

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'djangotoolbox',
    'autoload',
    'courrier',
    'dbindexer',
    'mediagenerator',
    'djangologging',
    'protobuf',
    'filetransfers',

    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)

MIDDLEWARE_CLASSES = (
    'mediagenerator.middleware.MediaMiddleware',
    
    # This loads the index definitions, so it has to come first
    'autoload.middleware.AutoloadMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware', # CACHE
    'django.middleware.csrf.CsrfViewMiddleware', # CSRF

    'django.middleware.common.CommonMiddleware', # CACHE
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'djangologging.middleware.LoggingMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

ADMIN_MEDIA_PREFIX = '/media/admin/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'

ROOT_MEDIA_FILTERS = {
    'js': 'mediagenerator.filters.yuicompressor.YUICompressor',
    'css': 'mediagenerator.filters.yuicompressor.YUICompressor',
}

YUICOMPRESSOR_PATH = os.path.join(os.path.dirname(__file__), 'yuicompressor-2.4.7.jar')

MEDIA_BUNDLES = (
     ('main.css',
        'css/main.css',
     ),
     ('main.js',
         {'filter': 'mediagenerator.filters.media_url.MediaURL'},
         'js/jquery.js',
     ),
)

MEDIA_DEV_MODE = DEBUG
DEV_MEDIA_URL = '/devmedia/'
PRODUCTION_MEDIA_URL = '/media/'

NOTIFICATION_SENDER = "notification@umitproject.org"
NOTIFICATION_TO = "notification@umitproject.org"
NOTIFICATION_REPLY_TO = "notification@umitproject.org"

GLOBAL_MEDIA_DIRS = (os.path.join(os.path.dirname(__file__), 'media'),)

INTERNAL_IPS = ('127.0.0.1', 'localhost',)
LOGGING_OUTPUT_ENABLED = True


# add support to user profile
AUTH_PROFILE_MODULE = 'users.UserProfile'
ACCOUNT_ACTIVATION_DAYS = 30
LOGIN_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
#'django.core.mail.backends.console.EmailBackend'

if on_production_server:
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'gmailusername@gmail.com'
    EMAIL_HOST_PASSWORD = 'xxxxxxx'
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = 'gmailusername@gmail.com'
    SERVER_EMAIL = 'gmailusername@gmail.com'
else:
    # local
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    DEFAULT_FROM_EMAIL = 'webmaster@localhost'

USE_I18N = True

SITENAME = "The Courrier"

##################
# RESPONSE COUNTS
MAX_NETLIST_RESPONSE = 10
MAX_AGENTSLIST_RESPONSE = 5

#########################
# File Transfer settings
PREPARE_UPLOAD_BACKEND = 'filetransfers.backends.delegate.prepare_upload'
PRIVATE_PREPARE_UPLOAD_BACKEND = 'djangoappengine.storage.prepare_upload'
PUBLIC_PREPARE_UPLOAD_BACKEND = 'djangoappengine.storage.prepare_upload'
SERVE_FILE_BACKEND = 'djangoappengine.storage.serve_file'
PUBLIC_DOWNLOAD_URL_BACKEND = 'filetransfers.backends.base_url.public_download_url'
PUBLIC_DOWNLOADS_URL_BASE = '/data/'
