import gevent.monkey

gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
from .celery import app as celery_app  # импортируем наш celery_app из файла celery.py
