"""
Запуск celery worker в отдельном процессе при запуске контейнера
"""

import gevent.monkey

gevent.monkey.patch_all()  # ⚠️ Первым!

from money_collect.celery import app

if __name__ == "__main__":
    app.worker_main(argv=["worker", "-l", "info", "-P", "gevent"])
