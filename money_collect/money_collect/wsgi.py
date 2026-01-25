"""
WSGI config for money_collect project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import gevent.monkey

gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "money_collect.settings")

application = get_wsgi_application()
