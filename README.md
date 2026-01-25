# API ДЛЯ ГРУППОВЫХ ДЕНЕЖНЫХ СБОРОВ

Доступные адреса
Главная страница (Swagger): http://localhost:8000/
Админ-панель:               http://localhost:8000/admin
API документация (Swagger): http://localhost:8000/swagger
API документация (ReDoc):   http://localhost:8000/redoc
REST API:                   http://localhost:8000/api/

Основные эндпоинты API
GET/POST /api/collects/ - список сборов и создание нового
GET/PUT/PATCH/DELETE /api/collects/{id}/ - детали сбора
POST /api/collects/{id}/donate/ - сделать пожертвование
GET /api/collects/{id}/payments/ - список пожертвований для сбора
GET /api/collects/active/ - активные сборы
GET/POST /api/payments/ - список платежей
GET/POST /api/users/ - пользователи
GET /api/users/me/ - текущий пользователь
Фильтрация и поиск
Фильтрация сборов по поводу: ?occasion=charity
Поиск по названию и описанию: ?search=помощь
Сортировка: ?ordering=-created_at
Активные сборы: /api/collects/active/

Структура папок
Серийный номер тома: 6CDE-263F
C:.
│   Dockerfile
│   entrypoint.sh
│   manage.py
│   README.md
│   requirements.txt
│   run_celery.py
│
├───api
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   serializers.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───management
│   │   │   __init__.py
│   │   │
│   │   ├───commands
│   │   │   │   fill_mockdata.py
│   │   │   │   fill_mockdataSQL.py
│   │   │   │   __init__.py
│   │   │   │
│   │   │   └───__pycache__
│   │   │           fill_mockdata.cpython-312.pyc
│   │   │           fill_mockdataSQL.cpython-312.pyc
│   │   │           __init__.cpython-312.pyc
│   │   │
│   │   └───__pycache__
│   │           __init__.cpython-312.pyc
│   │
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   0002_alter_collect_occasion_alter_payment_user.py
│   │   │   0003_alter_collect_end_date_alter_collect_occasion_and_more.py
│   │   │   0004_alter_collect_end_date_alter_collect_occasion.py
│   │   │   0005_alter_collect_collected_amount_and_more.py
│   │   │   0006_alter_collect_end_date.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           0001_initial.cpython-312.pyc
│   │           0002_alter_collect_occasion_alter_payment_user.cpython-312.pyc
│   │           0003_alter_collect_end_date_alter_collect_occasion_and_more.cpython-312.pyc
│   │           0004_alter_collect_end_date_alter_collect_occasion.cpython-312.pyc
│   │           0005_alter_collect_collected_amount_and_more.cpython-312.pyc
│   │           0006_alter_collect_end_date.cpython-312.pyc
│   │           __init__.cpython-312.pyc
│   │
│   ├───utils
│   │   │   email_utilities.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           email_utilities.cpython-312.pyc
│   │           __init__.cpython-312.pyc
│   │
│   └───__pycache__
│           admin.cpython-312.pyc
│           apps.cpython-312.pyc
│           models.cpython-312.pyc
│           serializers.cpython-312.pyc
│           urls.cpython-312.pyc
│           views.cpython-312.pyc
│           __init__.cpython-312.pyc
│
├───media
├───money_collect
│   │   asgi.py
│   │   celery.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
│   │   __init__.py
│   │
│   └───__pycache__
│           celery.cpython-312.pyc
│           settings.cpython-312.pyc
│           urls.cpython-312.pyc
│           wsgi.cpython-312.pyc
│           __init__.cpython-312.pyc
│
├───static
├───templates
│   └───api
│           collect_created.html
│           collect_created.txt
│           collect_updated.txt
│           payment_made.html
│           payment_made.txt
│           payment_updated.txt
│
└───__pycache__
        manage.cpython-312.pyc
        manage.cpython-313.pyc


__Установка модуля отладки DebugToolbar__
cd..
pip install django-debug-toolbar

# НАСТРОЙКИ ДЛЯ РАЗРАБОТКИ. НЕ ИСПОЛЬЗУЮТСЯ В РЕЖИМЕ ПРОДАКШН (самый нижний раздел в settings.py)
*************************************************************************************************
if DEBUG:
    # Регистрируем DjDT
    INSTALLED_APPS.append('debug_toolbar')
    # Добавляем константу для DjDT, чтобы он понимал - запросы с каких IP адресов надо обрабатывать
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
    # Добавляем прослойку для DjDT
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware",)  # Должен быть последним, для продакшена не используется
__Внесение обработчика из модуля DjDT в список адресов обработчиков запросов в файле urls.py__
***money_collect\money_collect\urls.py***
 #импорт модуля debug_toolbar
import debug_toolbar

 #Занести URL для DjDT в список всех адресов обработчиков запросов
urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls) ), # URL для обработчика из другого джанго-проекта
]


__# настройки консольного почтового сервера для отладки отправки уведомлений в разработке__
***money_collect\money_collect\settings.py***
Отладочный ВЫВОД В КОНСОЛЬ вместо реальной отправки по email-адресам
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Для отправки уведомления в консоль при отладке в разработке
DEFAULT_FROM_EMAIL = 'no-reply@example.com'   # Для отправки уведомления в консоль

# Настройки почтового сервера list.ru для отправки уведомлений, если проект развернут локально
if DATABASES["default"]["HOST"] == 'localhost':
    config = Config(RepositoryEnv(
            r'C:/Users/EvgenyMINI_S/PythonProjects/DjangoMoneyCollect/.env.dev'
                    )
            )
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.list.ru'  # SMTP сервер list.ru
EMAIL_PORT = 587  # Порт для подключения
EMAIL_USE_TLS = True  # Использование TLS шифрования
EMAIL_USE_SSL = False   # SSL не используется, так как порт 587 работает с TLS

# Настройки почтового сервера list.ru для отправки уведомлений, если проект развернут локально
Условный оператор маскирует локальный путь к файлу ".env.dev" настроек r'C:/Users/EvgenyMINI_S/PythonProjects/DjangoMoneyCollect/.env.dev' при разворачивании через Docker контейнер. 
Иначе возникнет исключение - "путь или файл не существует".
В docker-compose указан путь к  файлу ".env.dev": ./.env.dev
if DATABASES["default"]["HOST"] == 'localhost':
    config = Config(RepositoryEnv(
            r'C:/Users/EvgenyMINI_S/PythonProjects/DjangoMoneyCollect/.env.dev'
                    )
            )
    EMAIL_HOST_USER = config('EMAIL_USER')          # Ваш email адрес (указан в переменных окружения .env.dev)
    EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')  # Пароль от почтового ящика (указан в переменных окружения .env.dev)
    DEFAULT_FROM_EMAIL = config('EMAIL_USER')       # Адрес отправителя по умолчанию (указан в переменных окружения .env.dev

else:
    # Настройки почтового сервера для отправки уведомлений, если проект развернут в Docker
    EMAIL_HOST_USER = conf('EMAIL_USER')          # Ваш email адрес (указан в переменных окружения .env.dev)
    EMAIL_HOST_PASSWORD = conf('EMAIL_PASSWORD')  # Пароль от почтового ящика (указан в переменных окружения .env.dev)
    DEFAULT_FROM_EMAIL = conf('EMAIL_USER')       # Адрес отправителя по умолчанию (указан в переменных окружения .env.dev)    
    # print(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL)

**************************************************************************************************

ОТПРАВЛЯЕМ УВЕДОМЛЕНИЯ ПО ПОЧТЕ

Для реализации асинхронной отправки уведомлений о создании сбора и создании платежа
используем пакеты Celery и Redis.
Установка пакетов в python-окружении
(.venv) PS C:\........DjangoMoneyCollect\money_collect> pip install celery redis
Настройки для Celery в settings.py
    # Настройки для CELERY
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
Настройки для Celery в папке money_collect/money_collect
-создаём файл celery.py (Файл celery.py должен находиться на том же уровне, что и settings.py)
celery.py
from celery import Celery

app = Celery(
    'money_collect',                    # Имя проекта
    broker='redis://localhost:6379/0',  # Брокер для Celery (например, Redis) обеспечивает передачу задач в Redis (queue)
    backend='redis://localhost:6379/0'  # Бэкэнд для Celery (например, Redis) обеспечивает хранение результатов задач в Redis (cache)
    )
app.config_from_object('django.conf:settings', namespace='CELERY')  # Импортирует настройки из Django settings.py
app.autodiscover_tasks(related_name='email_utilities')              # Автоматически обнаруживает задачи в приложении
                                                                    # email_utilities.py и регистрирует их в Celery
Дополнительные настройки работы Celery
В среде Windows отсутствует Unix-механизм fork() (системный вызов для создания пула дочерних процессов) 
и Celery использует библиотеку billiard для эмуляции многопроцессовости.
Однако, из-за многочисленных ограничений безопасности Windows billiard может работать некорректно. 
Так и случилось в этом проекте - возникали ошибки работы billiard.
В связи с этим были использованы альтернативные асинхронные пулы, имитирующие управляемую системой многопоточность,
запуском параллельных корутин greenlets, управляемых Python.
Эти пулы требуют в своей работе патчи стандартных библиотек для возможности их использования в асинхронном режиме.
Патчирование стандартных библиотек должно производиться в Python-приложениях до их импорта.  
Попытка использовать пул eventlet тоже оказалась неудачной, а пул gevent работает пока корректно.
Установка gevent в окружении проекта
(.venv) PS C:..\money_collect> pip install gevent
Кроме этого, во всех Python-приложениях Django-проекта перед импортом модулей следует запускать процедуру
monkey-патчирования стандартных библиотек:
import gevent.monkey
gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.

После установки и настройки Celery и Redis запускаем их из консоли из папки приложения.
В команде для Celery указываем опции 
-А name     указывает на наше Django-приложение
-l info     устанавливает уровень логирования (info, debug...)
-P gevent   указывает асинхронный пул для параллельной обработки задач (eventlet, gevent)

(.venv) PS C:..\money_collect> redis-server
(.venv) PS C:..\money_collect> celery -A money_collect worker -l info -P gevent

Расширенный запуск celery (для продакшен)
(.venv) PS C:..celery -A money_collect worker -l info -P gevent --concurrency=4 --max-tasks-per-child=100
--concurrency=4   ко-во параллельных процессов
--max-tasks-per-child=100  максим.число выполненных задач, после которых celery будет перезапущен

Все задачи по отправке уведомлений и обработке сигналов на отправку объединены в одном Python-приложении
***money_collect\api\utils\email_utilities.py***
Задачи разделены на группы - задачи по отправке почты и задачи по обработке сигналов на отправку.
Для этого импортируем:
import gevent.monkey
gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
from django.core.mail import send_mail                  # Функция для отправки email, декорирующая упрощённое использование класса
                                                        # EmailMessage для более сложных сценариев
from smtplib import SMTPException
from django.template.loader import render_to_string     # Функция для рендера шаблона
from django.utils.html import strip_tags                # Функция для удаления html-тегов из текста

from money_collect.settings import DEFAULT_FROM_EMAIL   # Адрес отправителя из настроек settings.py
from api.models import Collect, Payment                 # Модели сбора и платежа
from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver

Шаблоны для email - простые текстовые для отладки при разработке. 
Помещаем в папке корня проекта templates в подпапке api, 
ПРИМЕР:
money_collect\templates\api\collect_created.txt
plaintext
Здравствуйте!
Ваш сбор успешно создан:
Название: {{ collect.title }}
Повод: {{ collect.occasion }}
Описание: {{ collect.description }}
Целевая сумма: {{ collect.target_amount }} руб.
Дата окончания: {{ collect.end_date }}
Спасибо за использование нашей платформы!

Отправка уведомлений выполняется асинхронно на основе встроенного в Django метода send_mail().
Асинхронная (Celery) функция для генерации отправляемых данных должна получать на вход id объекта, а не сам объект, 
т.к. асинхронный метод отправки не может обрабатывать json-сериализованные объекты.
ПРИМЕР:
@shared_task                                            # Декоратор для Celery для асинхронной отправки email
def send_collect_created(collect_id):                   # Функция для отправки уведомления, принимает id сбора
    collect = Collect.objects.get(pk=collect_id)        # Получение объекта сбора по id
    # Параметры для отправки email
    subject = 'Collect created successfully'            # Тема письма
    message = render_to_string('api/collect_created.txt', {'collect': collect}) # Шаблон письма
    plain_message = strip_tags(message)                 # Текст письма без html-тегов
    to_email = collect.author.email                     # Получатель письма
    
    # Отправка письма с помощью встроенной функции send_mail
    try:
        send_mail(
        subject,
        plain_message,
        DEFAULT_FROM_EMAIL,     # Отправитель из настроек settings.py
        [to_email],             # Cписок получателей
        html_message=message,   # HTML-версия письма с тегами (если требуется)
        fail_silently=False     # Не отключать уведомление о неудаче
    )
        return True
    except SMTPException as e:
        print(f"Ошибка при отправке email: {str(e)}")
    return False

Обработка сигналов на отправку уведомлений использует пакет Django signals.
В функциях-обработчиках реализована логика выбора отправки - создание нового или обновление прежнего объекта.
ПРИМЕР:
@receiver(post_save, sender=Collect)                                # Декоратор для сигнала post_save для модели Collect
def trigger_notify_collect(sender, instance, created, **kwargs):    # Обработчик сигнала, принимает экземпляр модели и флаг создания
    if created:
        send_collect_created.delay(instance.pk)                     # Вызов задачи для отправки уведомления о создании сбора
    else:
        send_collect_updated.delay(instance.pk)                     # Вызов задачи для отправки уведомления об обновлении сбора


# ЗАПОЛНЕНИЕ БАЗЫ МОКОВЫМИ ДАННЫМИ

Создаём Python-приложение money_collect\api\management\commands\fill_mockdataSQL.py, 
в котором наследуем класс BaseCommand для реализации функции создания фиктивных пользователей, сборов и платежей.
В папках management/, commands/ создаём приложения __init__.py, чтобы Python рассматривал их как пакеты.

В модуле fill_mockdataSQL.py перед заполнением БД очищаем таблицы базы от единичных тестовых записей и сбрасываем id-счётчики,
используя прямые SQL-запросы к БД из контекстного менеджера with.

with connection.cursor() as cursor:
    for table in ['auth_user', 'api_payment', 'api_collect']:
        cursor.execute(f'TRUNCATE TABLE {table} CASCADE')
        cursor.execute(f'ALTER SEQUENCE {table}_id_seq RESTART WITH 1')

Из-за требования большого числа (несколько тысяч) записей в БД создание каждой группы моковых данных выполнялось
через пакетный SQL-запрос с предварительной подготовкой в цикле FOR  IN RANGE() списка кортежей со значениями !ВСЕХ! обязательных полей.
Здесь надо учитывать, что обязательные поля БД postgres почти все (NOT NULL). В Django-модели эти ограничения могут быть более мягими,
но они не действуют, так как прямые SQL-запросы в БД летят мимо модели.

Пакетный SQL-запрос обеспечивался методом  execute_values() из библиотеки psycopg2.extras внутри контекстного менеджера with.
Это было вызвано тем, что метод cursor.execute() некорректно обрабатывает списки кортежей со значениями полей объектов.
Известно, что метод execute_values из psycopg2.extras по умолчанию разбивает данные на батчи по 100 записей. Это приводит к тому,
что метод cursor.fetchall() при генерации списка номеров id возвращает только первые 100 ID, а остальные остаются незаписанными.
Эта проблема для таблицы Collect (1000 записей) была решена разбиением вручную списка кортежей данных для массового заполнения БД
на батчи по 100 элементов с последующим циклом по батчам выполнения пакетных SQL-запросов с пополнением списка id номеров записей.
Таким образом, в списке будут все id-номера записей таблицы Collect.

Для безопасности - снижения риска "инъекций" посторонних SQL-запросов при удалённом обращении к БД -
выполнялся параметризованный запрос через VALUES c плейсхолдером %s.

Соединение с БД postgres обеспечивалось Django-утилитой connection.

Такой подход в десятки раз был быстрее, чем при использовании  метода save() Django-ORM, 
как выполнялось первоначально при тест-прогонах.  
Пакет объектов записывался в БД всего за 1 или несколько (при цикле батчам) SQL-запросов к БД.

Логика создания моковых данных:
1.Создание фиктивных пользователей. 
    Суперюзер создаём ORM командой create_user() для автоматического хеширования пароля.
    После записи пакета объектов-пользователей в Базу Данных создаётся список id пользователей user_ids.
2.Создание фиктивных сборов со случайным автором из списка user_ids, случайной причиной сбора
    из списка OCCASION_CHOICES модели Collect, случайной целевой суммой.
    После записи пакета объектов-сборов в Базу Данных создаётся список id сборов collect_ids.
3.Создание фиктивных платежей со случайным донатером из user_ids, случайным сбором из collect_ids,
    случайной сумой платежа.
Было создано 100 пользователей, 1000 сборов и 10000 платежей

fill_mockdataSQL.py
import gevent.monkey
gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection                        # Для очистки базы перед заполнением моковыми данными
from django.contrib.auth.hashers import make_password   # Для хеширования паролей
from django.utils import timezone                       # Для создания даты создания пользователя
from api.models import Collect, Payment
from psycopg2.extras import execute_values              # Для пакетного создания записей в БД
import random

    # Очистка таблиц и сброс последовательностей первичного ключа 
with connection.cursor() as cursor:
    for table in ['auth_user', 'api_payment', 'api_collect']:
        cursor.execute(f'TRUNCATE TABLE {table} CASCADE')
        cursor.execute(f'ALTER SEQUENCE {table}_id_seq RESTART WITH 1')


class Command(BaseCommand):
    help = 'Заполняем базу данных моковыми данными через SQL запросы'

    def handle(self, *args, **options):

        """Создание суперпользователя с id=1, ORM методом create_superuser"""
        User.objects.create_superuser(   # Создаем суперпользователя методом create_superuser 
            username='admin',
            email='admin@admin.com',
            password='password',    # Пароль вводится в виде строки, но будет хеширован методом make_password
        )
        self.stdout.write('Создан суперпользователь с id=1')# Выводим сообщение в консоль
        
        """Создание остальных пользователей через пакетный SQL запрос"""
        self.stdout.write('Создание пользователей...')
        users = []
        for i in range(2, 101):  # 99 новых пользователей
            username = f'user{i}'
            password = make_password('password')        # Хешируем пароль
            email = f'{username}@{username}.com'        # Создаем email для теста
            date_joined = f'{timezone.now()}'           # Дата создания пользователя
            # is_superuser = False                        # Все пользователи не суперпользователи
            # is_staff = False                            # Все пользователи не сотрудники
            # is_active = True                            # Все пользователи активны
            """Пополняем список кортежей с данными пользователей"""
            users.append((username, password, email, username, username, False, False, True, date_joined))   

        with connection.cursor() as cursor:
            # Используем 1 SQL запрос для пакетного создания пользователей со значениями полей из списка кортежей users
            # с помощью параметризованного запроса VALUES %s, который принимает список кортежей users
            # Работает функция execute_values из psycopg2.extras
            # !Все обязательные поля (NOT NULL), кроме id, должны быть заполнены! при SQL запросе
            execute_values(cursor,
            """
                INSERT INTO auth_user (
                username, 
                password, 
                email,
                first_name,
                last_name,
                is_superuser, 
                is_staff, 
                is_active,
                date_joined
                )
                VALUES %s
                RETURNING id
            """, users                                          # Список кортежей с данными пользователей
            )
            user_ids = [row[0] for row in cursor.fetchall()]    # Получаем список id пользователей для создания сборов и платежей
        self.stdout.write(f'Создано {len(user_ids)} пользователей') # Выводим сообщение в консоль

        """Создание фиктивных сборов через пакетный SQL запрос"""
        self.stdout.write('Создание фиктивных сборов...')
        occasions = Collect.OCCASION_CHOICES        # Получаем список причин сбора
        collects = []
        collects_number = 1000
        for _ in range(collects_number):
            author_id = random.choice(user_ids)                             # Выбираем случайного автора
            title = f'Сбор №{random.randint(1, 101)} author_id:{author_id}'# Имя сбоора с уникальным id автора и номером 
            occasion = random.choice(occasions)                             # Выбираем случайную причину сбора
            description = f"Описание для сбора {title}"                     # Описание сбора
            target_amount = round(random.uniform(5000, 10000))              # Целевая сумма от 5000.00 до 10000.00
            created_at = timezone.now()                                     # Дата создания сбора
            end_date = timezone.now() + timezone.timedelta(days=100)        # Дата завершения сбора (+100 дней)
            """Пополняем список кортежей с данными сборов"""
            collects.append((author_id, title, occasion, description, target_amount, created_at, end_date))

        def chunks(lst, n):
            """Разбиваем список на списки по n элементов"""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        with connection.cursor() as cursor:
            collect_ids = []                # Список id сборов
            # Используем несколько пакетных SQL запросов в цикле по батчам для пакетного создания сборов 
            # по значениям полей из списка кортежей collects
            for batch in chunks(collects, 100): # Создаём список collects списков по 100 элементов
                execute_values(cursor,
                """
                    INSERT INTO api_collect (author_id, title, occasion, description, target_amount, created_at, end_date)
                    VALUES %s
                    RETURNING id
                """, batch                                       # batch-cписок кортежей с данными сборов
                )
                collect_ids.extend([row[0] for row in cursor.fetchall()]) # Пополняем список id сборов для создания платежей
            
            self.stdout.write(f'Создано {len(collect_ids)} сборов') # Выводим сообщение в консоль

        """Cоздание фиктивных платежей через пакетный SQL запрос"""
        self.stdout.write('Создание фиктивных платежей...')
        payments = []
        for _ in range(10000):
            user_id = random.choice(user_ids)           # Выбираем случайного пользователя
            collect_id = random.choice(collect_ids)     # Выбираем случайный сбор
            amount = round(random.uniform(10, 1000))    # Случайная сумма от 10.00 до 100.00
            # Пополняем список кортежей с данными платежей
            payments.append((user_id, collect_id, amount))  

        with connection.cursor() as cursor:
            # Используем 1 SQL запрос для пакетного создания платежей по значениям полей из списка кортежей payments
            execute_values(cursor,
            """
                INSERT INTO api_payment (user_id, collect_id, amount)
                VALUES %s
            """, payments                                       # Список кортежей с данными платежей
            )
            self.stdout.write(f'Создано {len(payments)} платежей')  # Выводим сообщение в консоль

        """Обновление поля collected_amount в таблице сборов Collect SQL запросом"""
        self.stdout.write('Обновление поля collected_amount в таблице сборов...') # Выводим сообщение в консоль
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE api_collect c
                           SET collected_amount = p.amount
                           FROM (
                                SELECT collect_id, SUM(amount) AS amount
                                FROM api_payment
                                GROUP BY collect_id
                            ) p
                            WHERE c.id = p.collect_id;
                            """)
            self.stdout.write('Поле collected_amount обновлено...') # Выводим сообщение в консоль

# ОСНОВНЫЕ СУЩНОСТИ ПРИЛОЖЕНИЯ MONEYCOLLECT

МОДЕЛИ

МОДЕЛЬ User
встроенная модель пользователей User.
Все авторы сборов и донатеры - это пользователи.

МОДЕЛЬ Collect
поля модели
OCCASION_CHOICES = [
        ('birthday', 'День рождения'),
        ('wedding', 'Свадьба'),
        ('medical', 'Лечение'),
        ('charity', 'Благотворительность'),
        ('emergency', 'Чрезвычайная ситуация'),
        ('other', 'Другое'),
    ]
    author = models.ForeignKey(User,... )
    title = 
    occasion = 
    description = 
    target_amount = 
    collected_amount = 
    cover_image = 
    end_date = 
    created_at =
    updated_at =

методы модели
    @property                       # Декоратор позволяющий получить значение свойства без SQL запроса по имени функции
    def is_active(self):
        if self.end_date > timezone.now() and self.target_amount > self.collected_amount:
            return  True            # если дата завершения больше текущей даты и сумма меньше цели, то is_active = True
        else: return False
    
    @property                        # Декоратор позволяющий получить значение свойства без SQL запроса по имени функции
    def payments_count(self):
        return self.payments.count()    # Подсчёт количества всех поступивших платежей в сборе. 
                                        # Применение collect.payments_count (collect - это объект модели Collect)

В таблице Collect (api_collect) поле collected_amount динамически изменяется в зависимости 
от поступивших в сбор платежей, сохранённых в таблице Payment (api_payment).
Для корректного изменения поля collected_amount таблицы api_collect в условиях множества 
одновременно поступающих платежей в модели Payment был реализован метод атомарного обновления этого поля
с использованием Django-инструмента models.F() для работы с выделенным полем таблицы 
на уровне базы данных (без предварительной загрузки в Python-объект и т.д.)

МОДЕЛЬ Payment
поля модели
    collect = models.ForeignKey(Collect,...)
    user = models.ForeignKey(User,...)
    amount = 
    comment = 
    created_at = 
    is_anonymous =

методы модели
импортируем инструмент F()
from django.db.models import F

    def __str__(self):
        return f'{self.user.username} - {self.amount}'

    def __init__(self, *args, **kwargs):    # Инициализация объекта класса Payment
        super().__init__(*args, **kwargs)   # Вызов конструктора родительского класса
        self._original_amount = self.amount # В объекте self._original_amount сохраняем сумму последнего платежа

    # Переопределяем метод save для обновления суммы сбора при создании нового платежа или изменении прежнего платежа
    def save(self, *args, **kwargs):
        is_new = self.pk is None                # Проверка на создание нового платежа (есть ли id)
        super().save(*args, **kwargs)           # Вызываем метод родительского класса и сохраняем в БД платеж
        # Обновляем сумму сбора при создании нового платежа
        if is_new:
            # Атомарно увеличиваем поле суммы сбора без явного сохранения объекта (так как всё происходит на уровне БД)
            # collect_id (id связанного объекта сбора collect) будет доступен, так как объект уже был сохранён
            Collect.objects.filter(pk=self.collect_id).update(
                collected_amount=F('collected_amount') + self.amount
            )
        else:
            # Существующий платёж: корректируем сумму сбора по разнице между прежним и текущим значением платежа
            if self._original_amount != self.amount:
                delta = self.amount - self._original_amount
                Collect.objects.filter(pk=self.collect_id).update(
                    collected_amount=F('collected_amount') + delta
                )
        self._original_amount = self.amount  # Обновляем прежнее значение платежа на текущее


ПАГИНАЦИЯ АВТОРИЗАЦИЯ ПОИСК ФИЛЬТРАЦИЯ СОРТИРОВКА
Все эти настройки были выполнены встроенными методами пакетов DRF 

В API настроен стиль постраничной пагинации вывода по 20 записей на страницу.
admin: доступен только авторизованным пользователям.
API: неавторизованным пользователям доступен только просмотр.
Для выбора вариантов поиска, фильтрации и сортировки доступна кнопка "Фильтрация" в окне списков объектов.
Поля поиска, фильтриции и сорировки заданы во вьюсетах \money_collect\api\views.py
settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
],
}

CORS 
Установлен и на время отладки был настроен разрешение запросов всех доменов
settings.py
INSTALLED_APPS = [
    'corshaeders'
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",    # Поле для CORS должно быть первым
............................
]
settings.py
    CORS_ALLOW_ALL_ORIGINS = True

API ПРЕДСТАВЛЕНИЯ

Для создания API представлений использовалась библиотека DRF viewsets
В представлениях наcтраивались CRUD операции  в завсисимости от модели и прав пользователя,
а также поля фильтрации, поиска и сортировки при необходимости изменить умолчания, 
настроенные в settings.py.
Дополнительные фунцкии операций с объектами настраивались с декоратором @action.

USER 
методы 'POST', 'PUT', 'DELETE' доступны только админу.
Остальным пользователям доступен просмотр.

UserViewSet
шаблон при выводе списка пользователей
методы
def get_permissions(self):                                  # Переопределяем метод для установки прав доступа
def get_serializer_class(self):                             # Переопределяем функцию для выбора сериализатора
                                                        в зависимости от действия
COLLECT
CRUD операции доступны авторизованным пользователям

CollectViewSet
шаблон при создании пользователя
Поля поиска, фильтрации, сортиовки
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]   # Для фильтрации, поиска и сортировки по на API-странице сборов
    filterset_fields = ['occasion', 'author']                               # Поля фильтрации
    search_fields = ['title', 'description']                                # Поля поиска. Поиск будет по полям title и description
    ordering_fields = ['created_at', 'collected_amount', 'end_date']
методы

    # Выбор сериалайзера данных для списка сборов в зависимости от действия 
def get_serializer_class(self):

    # Функция для создания сбора (и отправка уведомления, если не используются сигналы - закоммичено)
def def perform_create(self, serializer):

    # Extra Action 'Donate' на уровне API конкретного сбора (detail=True)
    # Ввод нового платежа, доступен POST-запрос для авторизованных пользователей
@action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
def donate(self, request, pk=None):                         # Отправка POST-запроса на платёж на API-странице сбора

    # Extra Action 'Payments' на уровне API конкретного сбора (detail=True)
    # Вывод всех платежей на уровне API только для текущего сбора, доступно только при GET-запросе
@action(detail=True, methods=['get'])
def payments(self, request, pk=None):

    # Extra Action 'Active' на уровне API списка сборов, доступно при GET-запросе
    # Вывод всех (detail=False) активных сборов на странице
@action(detail=False, methods=['get'])
def active(self, request):


PaymentViewSet
шаблон для вывода платежей пользователя
CRUD операции доступны авторизованным пользователям
методы
def get_queryset(self):                   # Переопределяется запрос платежей с фильтрацией по текущему пользователю

    # Функция для создания платежа: сбор и донатер на выбор (и отправка уведомления, если не используются сигналы)
def perform_create(self, serializer):


СЕРИАЛИЗАТОРЫ
Сериализаторы выполнены с использованием встроенного класса ModelSerializer

UserSerializer
сериализатор просмотра списка пользователей

UserCreateSerializer
сериализатор при создании пользователя
        # Метод создаёт пользователя с хешированным паролем, если данные валидны
        использует встроенный метод create_user
def create(self, validated_data):

CollectSerializer
для вывода сбора по id
на странице сбора доступна операция PUT обновления сбора
методы
def get_cover_image_url(self, obj):         # Получение URL обложки платежа для вывода в API 
def validate_end_date(self, value):         # Валидация даты сбора

CollectListSerializer
для вывода списка сборов
методы
def get_cover_image_url(self, obj):         # Получение URL обложки сбора для вывода в API
def get_progress_percentage(self, obj):     # Расчёт %% текущей суммы от цели сбора для вывода в API

PaymentSerializer
для вывода списка платежей пользоваателя и платежа по id 
методы
def to_representation(self, instance):      # Переопределяем формат вывода анонимного платежа - указываем значения полей модели.

PaymentCreateSerializer
для создания нового платежа, вызывается из CollectViewSet в методе donate()


URLS

money_collect\money_collect\urls.py
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('swagger', cache_timeout=0)), # Главная страница - Swagger
    path('__debug__/', include(debug_toolbar.urls) ), # URL для обработчика из другого джанго-проекта. Не использовать в продакшен
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

money_collect\api\urls.py
router = DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')
router.register(r'collects', views.CollectViewSet, basename='collect')
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
path('', include(router.urls)),
]

# DOCKER-КОНТЕЙНЕРИЗАЦИЯ

DOCKER_COMPOSE
Для настройки работы контейнеров с Redis и Celery добавим эти сервисы в docker-compose.yml
и настроим окружения:

***docker-compose.yml***
services:
  web:
    build: ./money_collect  # образ сервиса web будет создан в директории контейнера /usr/src/money_collect из Dockerfile  в текущей директории на диске
    command: python manage.py runserver 0.0.0.0:8000
    volumes:                              # Тома этого сервиса
      - ./money_collect/:/usr/src/money_collect
    ports:                                # Сопоставление портов хоста и контейнера
      - 8000:8000
    env_file:                             # переменные окружения из файла ".env.dev"
      - ./.env.dev
    environment:                        # переменные окружения в явном виде
      CELERY_BROKER_URL: redis://redis:6379/0       # адрес брокера сообщений, который используется Celery для управления очередями
      CELERY_RESULT_BACKEND: redis://redis:6379/0   # адрес для хранения результатов задач
    depends_on:                         # Сервиса web будет запущен, если сервис db заработал
      - redis
      - db  #: condition: service_healthy

  celery:
    build: ./money_collect
    command: celery -A money_collect worker -l info -P gevent
    depends_on:
      - redis
      - db
    env_file:                             # переменные окружения из файла ".env.dev"
      - ./.env.dev
    environment:
      CELERY_BROKER_URL: redis://redis:6379/0
      CELERY_RESULT_BACKEND: redis://redis:6379/0
      DATABASE_URL: postgresql://postgres:postgres@db:5432/mydatabase

  redis:
    image: redis:7.4
    ports:
      - "6379:6379"

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: moneycollect

volumes:
  postgres_data:


Dockerfile
Создание Dockerfile было описано в ДЗ_7

***money_collect\Dockerfile***
FROM python:3.12-slim
WORKDIR /usr/src/money_collect/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && \
    apt-get install -y \
    curl \
    postgresql-client
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/money_collect/entrypoint.sh
RUN chmod +x /usr/src/money_collect/entrypoint.sh
COPY . .
ENTRYPOINT ["/usr/src/money_collect/entrypoint.sh"]

***money_collect\entrypoint.sh***
#!/bin/bash

wait_for_postgres() {                           # Функция ожидания PostgreSQL.
    if [[ "$DATABASE" == "postgres" ]]; then    # Если база данных PostgreSQL,
        echo "Ожидание PostgreSQL..."           # то выводится сообщение.
        # Пока не подключится к postgresql-client, идёт цикл. с паузой 1 сек.
        while ! pg_isready -h $SQL_HOST -U $SQL_USER; do                 # Если postgresql-client установлен в Dockerfile
        # while ! curl --silent --head --fail http://$SQL_HOST:5432; do   # Если curl установлен в Dockerfile
        # while ! nc -z $SQL_HOST 5432; do                                # Если postgresql-client, curl не установлены
            sleep 1
            echo "Ожидание PostgreSQL..."                                   # Отладочный вывод в консоли Docker
            echo "POSTGRES_HOST: "$SQL_HOST, "POSTGRES_PORT: "$SQL_PORT     # Отладочный вывод в консоли Docker
        done
        echo "POSTGRES_HOST: "$SQL_HOST, "POSTGRES_PORT: "$SQL_PORT         # Отладочный вывод в консоли Docker
        echo "PostgreSQL готов"
    fi
}

create_db() {                             
    echo "Проверка наличия базы данных " $SQL_DATABASE
    if PGPASSWORD="$SQL_PASSWORD" psql -h "$SQL_HOST" -U "$SQL_USER" -c "SELECT 1 FROM pg_database WHERE datname = '$SQL_DATABASE'" | grep -q 1; then
        echo "База данных ", $SQL_DATABASE, " уже существует"
    else
        PGPASSWORD="$SQL_PASSWORD" psql -h "$SQL_HOST" -U "$SQL_USER" -c "CREATE DATABASE '$SQL_DATABASE'"
        if [ $? -eq 0 ]; then
            echo "База данных ", $SQL_DATABASE, " успешно создана"
        else
            echo "Ошибка создания базы данных ", $SQL_DATABASE
            exit 1
        fi
    fi
}
if [[ "$DATABASE" == "sqlite" ]]; then  # Если база данных SQLite,
    DB_PATH = "./db.sqlite3"
    if [[ ! -f DB_PATH ]]; then      # Если по адресу ($DB_PATH) файл (-f) базы данных не (!) существует,
        touch DB_PATH                # то создаётся пустой файл db.sqlite3.
        chmod 666 DB_PATH            # и его права на чтение и запись (666) для всех пользователей.
    fi
Обработка PostgreSQL
elif [[ "$DATABASE" == "postgres" ]]; then  # Если база данных PostgreSQL,
    wait_for_postgres                       # Выполняется функция ожидания PostgreSQL.
    create_db                         # Выполняется функция проверки наличия и создания пустой базы данных в случае отсутствия.
fi
python manage.py migrate 
#python manage.py runserver 0.0.0.0:8000
exec "$@"

# ТЕСТОВЫЙ РЕЖИМ С МОКОВЫМИ ДАННЫМИ БД - ПОДГОТОВКА В ЗАПУСКУ И ЗАПУСК КОНТЕЙНЕРОВ ИЗ DOCKER-COMPOSE

0.Отключаем DEBUG TOOLBAR (комментируем строки с debug_toolbar)
***money_collect\money_collect\settings.py***
    #"debug_toolbar.middleware.DebugToolbarMiddleware", 
    #"debug_toolbar",       
***money_collect\money_collect\urls.py***
    # import debug_toolbar                        # Импортируем для отладки. Для продакшена закомментировать
    # path("__debug__/", include(debug_toolbar.urls)), 

1.сохраняем зависимости
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoMoneyCollect\money_collect> pip freeze > requirements.txt

2.Запускаем на компьютере с Windows приложение Docker_Desktop

3.Запуск docker-compose из папки с  docker-compose.yml
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoMoneyCollect> docker-compose up -d --build

ПОСЛЕ ЗАПУСКА КОНТЕЙНЕРА ИЗ КОНСОЛИ ПРИЛОЖЕНИЯ DOCKER-DESKTOP:
Если базы нет, то создаём суперюзера, ещё раз проверяем миграциии 
и запускаем заполнение базы моковыми данными.
здесь aeb2bba2939e это ID web-контейнера
PS C:\Users\EvgenyMINI_S> docker exec -it aeb2bba2939e<(WEB-КОНТЕЙНЕР ID) bash -c "python /usr/src/money_collect/manage.py createsuperuser"
PS C:\Users\EvgenyMINI_S> docker exec -it aeb2bba2939e bash -c "python /usr/src/money_collect/manage.py makemigrations"
PS C:\Users\EvgenyMINI_S> docker exec -it aeb2bba2939e bash -c "python /usr/src/money_collect/manage.py migrate"
PS C:\Users\EvgenyMINI_S> docker exec -it aeb2bba2939e bash -c "python /usr/src/money_collect/manage.py fill_mockdataSQL"

# ДПОПЛНИТЕЛЬНЫЕ ФИЧИ ПРОЕКТА MONEYCOLLECT

# Django Extensions
это набор полезных команд и утилит для разработки на Django.
Они включают в себя команды для работы с базой данных, генерации диаграмм моделей и многое другое.

Установка:
(venv) pip install django-extensions
Чтобы делать диаграмму в виде изображения:
(venv) pip install pydotplus

Настройка:
добавить 'django_extensions' в список INSTALLED_APPS.

Пример использования команды для генерации диаграммы моделей:
С помощью этой команды вы можете визуализировать
структуру вашей базы данных, что особенно полезно при
работе с большими и сложными проектами.
(venv) python manage.py graph_models -a -o models.png

Настройка шрифта settings.py, используемого утилитой graph_models
GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
    'output': 'png',
    'arrow_shape': 'open',
    'fontname': 'Arial',  # Устанавливаем по умолчанию доступный в системе шрифта (исходный шрифт ROBOTO)
}

# ЗАПУСК ПРИЛОЖЕНИЯ с БД в localhost или в docker-контейнере

Приложение можно запускать в режиме локальной равёртки или разворачиать в Docker контейнере
Для выбора варианта реализовано условие по значению параметра сервера ДБ postgres
***money_collect\money_collect\settings.py***
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "moneycollect",
        "USER": "postgres",
        "PASSWORD": "postgres",
        # "HOST": "localhost",
        # "HOST": "db",         # Имя контейнера с БД db, использовать вместо localhost при развертывании в Docker
        "PORT": "5432",

    }
}


1.Разворачивание приложения через localhost
a.  раскомичиваем 'localhost' в settings.py
        "HOST": "localhost",
        # "HOST": "db",         # Имя контейнера с БД db, использовать вместо localhost при развертывании в Docker
b. в консоли из  корневой папки приложения \money_collect\ запускаем Celery
        (.venv) .....\DjangoMoneyCollect\money_collect> celery -A money_collect worker -l info -P gevent
c. запускаем сервер из корневой папки приложения \money_collect\
        (.venv) ......\DjangoMoneyCollect\money_collect> py -m manage runserver

2.Разворачивание приложения через Docker
a.  раскомичиваем 'db' в settings.py
        # "HOST": "localhost",
        "HOST": "db",         # Имя контейнера с БД db, использовать вместо localhost при развертывании в Docker
b.  в среде windows из меню компа запускаем Docker Desktop (GUI Docker Desktop + Linux подсистема в windows WSL2)
("C:\Program Files\Docker\Docker\Docker Desktop.exe")
c.  в консоли из папки над корневой (из папки, где расположены docker-compose.yml и .env.dev), запускаем docker-compose.yml
        (.venv) .....\DjangoMoneyCollect> docker-compose up -d --build

НАСТРОЙКА ЗАПУСКА CELERY В КОНТЕЙНЕРЕ ОТ ИМЕНИ НЕПРИВИЛЕГИРОВАННОГО ПОЛЬЗОВАТЕЛЯ (необходимо для продакшн)

а. в Dockerfile создаём группу celerygroup и пользователя celeryuser с предварительной проверкой их существования
    getent group celerygroup - получение информации из системной базы данных групп о группе celerygroup
    getent passwd celeryuser - получение информации о пользователе celeryuser из системной базы данных паролей
    >/dev/null - подавление вывода любых сообщений (вывод в несуществующий каталог)
    groupadd -r celerygroup - создание системной (-r) группы
    useradd -m -r -g celerygroup celeryuser - создание в группе пользователя
        -m  создает домашний каталог пользователя
        -r  создает системного пользователя
        -g  указывает основную группу пользователя
***money_collect\Dockerfile***
    # Проверяем существование группы и пользователя перед созданием (первые строки после FROM python..)
RUN if ! getent group celerygroup >/dev/null; then groupadd -r celerygroup; fi
RUN if ! getent passwd celeryuser >/dev/null; then useradd -m -r -g celerygroup celeryuser; fi

после команды COPY рабочего каталога
    # Установка разрешений на рабочий каталог-Переключение на пользователя celeryuser-Запуск Celery worker
RUN chown -R celeryuser:celerygroup /usr/src/money_collect
USER celeryuser
CMD ["celery", "-A", "money_collect", "worker", "-l", "info", "-P", "gevent"]
