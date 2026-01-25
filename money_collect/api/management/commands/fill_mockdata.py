import gevent.monkey
gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import \
    connection  # Для очистки базы перед заполнением моковыми данными

from api.models import Collect, Payment

# Очистка таблиц и сброс последовательностей первичного ключа
with connection.cursor() as cursor:
    for table in ["auth_user", "api_payment", "api_collect"]:
        cursor.execute(f"TRUNCATE TABLE {table} CASCADE")
        cursor.execute(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1")


class Command(BaseCommand):
    # Функция заполнения базы данных моковыми данными
    def handle(self, *args, **options):
        users = []  # Список пользователей
        collects = []  # Список сборов
        payments = []  # Список платежей

        # Генерация пользователей
        for i in range(3, 11):  # Два пользователя уже есть
            username = f"user{i}"
            password = f"password"
            email = f"{username}@{username}.com"
            new_user = User(username=username)
            new_user = User(email=email)
            new_user.set_password(password)
            new_user.save()
            users.append(new_user)

        # Создание фиктивных сборов
        occasions = Collect.OCCASION_CHOICES  # Получаем список причин сбора
        for _ in range(10):
            author = random.choice(users)
            title = f"Сбор {author} №{random.randint(1, 100)}"
            occasion = random.choice(occasions)
            description = f"Описание для сбора #{title}"
            collect = Collect(
                author=author, title=title, occasion=occasion, description=description
            )
            collect.save()
            collects.append(collect)

        # Cоздание фиктивных платежей
        for _ in range(50):
            collection = random.choice(collects)
            user = random.choice(users)
            amount = round(random.uniform(10, 1000), 2)
            payment = Payment(user=user, collect=collection, amount=amount)
            payment.save()
            payments.append(payment)
