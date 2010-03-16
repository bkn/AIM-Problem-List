import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'aimpl.settings'

from django.core.management import setup_environ
from aimauth import settings
setup_environ(settings)

import django.core.handlers.wsgi
from django.core.servers.basehttp import AdminMediaHandler

application = AdminMediaHandler(django.core.handlers.wsgi.WSGIHandler())

import tornado
import tornado.httpserver
import tornado.wsgi

container = tornado.wsgi.WSGIContainer(application)
http_server = tornado.httpserver.HTTPServer(container)
http_server.listen(8000)
tornado.ioloop.IOLoop.instance().start()
