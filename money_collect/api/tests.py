import gevent.monkey

gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
from django.test import TestCase

# Create your tests here.
