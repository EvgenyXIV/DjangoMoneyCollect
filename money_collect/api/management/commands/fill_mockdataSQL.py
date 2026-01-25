import gevent.monkey

gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
import random

from django.contrib.auth.hashers import \
    make_password  # Для хеширования паролей
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import \
    connection  # Для очистки базы перед заполнением моковыми данными
from django.utils import timezone  # Для создания даты создания пользователя
from psycopg2.extras import \
    execute_values  # Для пакетного создания записей в БД

from api.models import Collect, Payment

# Очистка таблиц и сброс последовательностей первичного ключа
with connection.cursor() as cursor:
    for table in ["auth_user", "api_payment", "api_collect"]:
        cursor.execute(f"TRUNCATE TABLE {table} CASCADE")
        cursor.execute(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1")


class Command(BaseCommand):
    help = "Заполняем базу данных моковыми данными через SQL запросы"

    def handle(self, *args, **options):
        """Создание суперпользователя с id=1, ORM методом create_superuser"""
        User.objects.create_superuser(  # Создаем суперпользователя методом create_superuser
            username="admin",
            email="admin@admin.com",
            password="password",  # Пароль вводится в виде строки, но будет хеширован методом make_password
        )
        self.stdout.write(
            "Создан суперпользователь с id=1"
        )  # Выводим сообщение в консоль

        """Создание остальных пользователей через пакетный SQL запрос"""
        self.stdout.write("Создание пользователей...")
        users = []
        for i in range(2, 101):  # 99 новых пользователей
            username = f"user{i}"
            password = make_password("password")  # Хешируем пароль
            email = f"{username}@{username}.com"  # Создаем email для теста
            date_joined = f"{timezone.now()}"  # Дата создания пользователя
            # is_superuser = False                        # Все пользователи не суперпользователи
            # is_staff = False                            # Все пользователи не сотрудники
            # is_active = True                            # Все пользователи активны
            """Пополняем список кортежей с данными пользователей"""
            users.append(
                (
                    username,
                    password,
                    email,
                    username,
                    username,
                    False,
                    False,
                    True,
                    date_joined,
                )
            )

        with connection.cursor() as cursor:
            # Используем 1 SQL запрос для пакетного создания пользователей со значениями полей из списка кортежей users
            # с помощью параметризованного запроса VALUES %s, который принимает список кортежей users
            # Работает функция execute_values из psycopg2.extras
            # !Все обязательные поля (NOT NULL), кроме id, должны быть заполнены! при SQL запросе
            execute_values(
                cursor,
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
            """,
                users,  # Список кортежей с данными пользователей
            )
            user_ids = [
                row[0] for row in cursor.fetchall()
            ]  # Получаем список id пользователей для создания сборов и платежей
        self.stdout.write(
            f"Создано {len(user_ids)} пользователей"
        )  # Выводим сообщение в консоль

        """Создание фиктивных сборов через пакетный SQL запрос"""
        self.stdout.write("Создание фиктивных сборов...")
        occasions = Collect.OCCASION_CHOICES  # Получаем список причин сбора
        collects = []
        collects_number = 1000
        for _ in range(collects_number):
            author_id = random.choice(user_ids)  # Выбираем случайного автора
            title = f"Сбор №{random.randint(1, 101)} author_id:{author_id}"  # Имя сбоора с уникальным id автора и номером
            occasion = random.choice(occasions)  # Выбираем случайную причину сбора
            description = f"Описание для сбора {title}"  # Описание сбора
            target_amount = round(
                random.uniform(5000, 10000)
            )  # Целевая сумма от 5000.00 до 10000.00
            created_at = timezone.now()  # Дата создания сбора
            end_date = timezone.now() + timezone.timedelta(
                days=100
            )  # Дата завершения сбора (+100 дней)
            updated_at = timezone.now()
            """Пополняем список кортежей с данными сборов"""
            collects.append(
                (
                    author_id,
                    title,
                    occasion,
                    description,
                    target_amount,
                    created_at,
                    updated_at,
                    end_date,
                )
            )

        def chunks(lst, n):
            """Разбиваем список на списки по n элементов"""
            for i in range(0, len(lst), n):
                yield lst[i : i + n]

        with connection.cursor() as cursor:
            collect_ids = []  # Список id сборов
            # Используем несколько пакетных SQL запросов в цикле по батчам для пакетного создания сборов
            # по значениям полей из списка кортежей collects
            for batch in chunks(
                collects, 100
            ):  # Создаём список collects списков по 100 элементов
                execute_values(
                    cursor,
                    """
                    INSERT INTO api_collect (author_id, title, occasion, description, target_amount, created_at, updated_at, end_date)
                    VALUES %s
                    RETURNING id
                """,
                    batch,  # batch-cписок кортежей с данными сборов
                )
                collect_ids.extend(
                    [row[0] for row in cursor.fetchall()]
                )  # Пополняем список id сборов для создания платежей

            self.stdout.write(
                f"Создано {len(collect_ids)} сборов"
            )  # Выводим сообщение в консоль

        """Cоздание фиктивных платежей через пакетный SQL запрос"""
        self.stdout.write("Создание фиктивных платежей...")
        payments = []
        for _ in range(10000):
            amount = round(
                random.uniform(10, 1000)
            )  # Случайная сумма от 10.00 до 100.00
            comment = f"Описание платежа..."
            created_at = timezone.now()  # Дата создания платежа
            collect_id = random.choice(collect_ids)  # Выбираем случайный сбор
            is_anonymous = False
            user_id = random.choice(user_ids)  # Выбираем случайного пользователя

            # Пополняем список кортежей с данными платежей
            payments.append(
                (amount, comment, created_at, is_anonymous, collect_id, user_id)
            )

        with connection.cursor() as cursor:
            # Используем 1 SQL запрос для пакетного создания платежей по значениям полей из списка кортежей payments
            execute_values(
                cursor,
                """
                INSERT INTO api_payment (amount, comment, created_at, is_anonymous, collect_id, user_id)
                VALUES %s
            """,
                payments,  # Список кортежей с данными платежей
            )
            self.stdout.write(
                f"Создано {len(payments)} платежей"
            )  # Выводим сообщение в консоль

        """Обновление поля collected_amount в таблице сборов Collect SQL запросом"""
        self.stdout.write(
            "Обновление поля collected_amount в таблице сборов..."
        )  # Выводим сообщение в консоль
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE api_collect c
                           SET collected_amount = p.amount
                           FROM (
                                SELECT collect_id, SUM(amount) AS amount
                                FROM api_payment
                                GROUP BY collect_id
                            ) p
                            WHERE c.id = p.collect_id;
                            """
            )
            self.stdout.write(
                "Поле collected_amount обновлено..."
            )  # Выводим сообщение в консоль
