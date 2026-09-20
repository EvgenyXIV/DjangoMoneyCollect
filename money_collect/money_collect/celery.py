from __future__ import (
    absolute_import,
    unicode_literals,
)  # Для совместимости с Python 2 и 3
import gevent.monkey

gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "money_collect.settings")
app = Celery(
    "money_collect",  # Имя проекта
    # Настройки broker и backend указаны в settings.py
    # broker="redis://localhost:6379/0",  # Брокер для Celery (например, Redis) обеспечивает передачу задач в Redis (queue)
    # backend="redis://localhost:6379/0",  # Бэкэнд для Celery (например, Redis) обеспечивает хранение результатов задач в Redis (cache)
)
app.config_from_object(
    "django.conf:settings", namespace="CELERY"
)  # Импортирует настройки из Django settings.py
app.autodiscover_tasks(
    related_name="email_utilities"
)  # Автоматически обнаруживает задачи в приложении email_utilities.py и регистрирует их в Celery
# app.conf.worker_pool = 'eventlet'    # Используем eventlet для обработки задач в Celery вместо billiard
