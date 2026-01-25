import gevent.monkey

gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.
from django.db import models
from django.db.models import (
    F,
)  # Этот инструмент F() участвует в обновлении суммы сбора поле collected_amount
from django.contrib.auth.models import User
from django.utils import timezone  # Для установки и проверки даты завершения сбора

# Create your models here.


class Collect(models.Model):
    OCCASION_CHOICES = [
        ("birthday", "День рождения"),
        ("wedding", "Свадьба"),
        ("medical", "Лечение"),
        ("charity", "Благотворительность"),
        ("emergency", "Экстреная ситуация"),
        ("other", "Другое"),
    ]
    author = models.ForeignKey(  # Авторы сборов - это пользователи
        User,
        on_delete=models.CASCADE,
        related_name="collects",
        verbose_name="Автор сбора",
    )
    title = models.CharField(max_length=200, verbose_name="Название сбора")
    occasion = models.CharField(
        max_length=40,
        choices=OCCASION_CHOICES,
        default="charity",
        verbose_name="Повод сбора",
    )
    description = models.TextField(verbose_name="Описание сбора")
    target_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        default=100000,
        verbose_name="Целевая сумма",
    )
    collected_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
        verbose_name="Собранная сумма",
    )
    cover_image = models.ImageField(
        upload_to="covers/", null=True, blank=True, verbose_name="Витрина сбора"
    )
    end_date = models.DateTimeField(
        default=timezone.datetime(2029, 12, 31), verbose_name="Дата завершения сбора"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания сбора"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления сбора"
    )

    class Meta:
        verbose_name = "Групповой сбор"
        verbose_name_plural = "Групповые сборы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property  # Декоратор позволяющий получить значение свойства по имени функции без SQL запроса
    def is_active(self):  # Флаг активности сбора
        if self.end_date > timezone.now():
            return True  # если дата завершения больше текущей даты, то is_active = True
        else:
            return False
        # if self.collected_amount and self.target_amount != 0:
        #     if self.end_date > timezone.now() and self.target_amount > self.collected_amount:
        #         return  True        # если дата завершения больше текущей даты и текущая сумма сбора меньше цели, то is_active = True
        #     else: return False
        # else:
        #     if self.end_date > timezone.now() and self.target_amount == 0:
        #        return  True        # если дата завершения больше текущей даты
        #     else: return False

    @property  # Декоратор позволяющий получить значение свойства по имени функции без SQL запроса
    def payments_count(self):
        return (
            self.payments.count()
        )  # Подсчёт количества всех поступивших платежей в сборе.
        # Применение collect.payments_count (collect - это объект модели Collect)


class Payment(models.Model):
    collect = models.ForeignKey(
        Collect, on_delete=models.CASCADE, related_name="payments", verbose_name="Сбор"
    )
    user = models.ForeignKey(  # Донатеры это пользователи, которые сделали платёж
        User, on_delete=models.CASCADE, related_name="payments", verbose_name="Донатер"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма платежа"
    )
    comment = models.TextField(blank=True, verbose_name="Комментарий к платежу")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время платежа"
    )
    is_anonymous = models.BooleanField(default=False, verbose_name="Анонимный платеж")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

    def __init__(self, *args, **kwargs):  # Инициализация объекта класса Payment
        super().__init__(*args, **kwargs)  # Вызов конструктора родительского класса
        self._original_amount = (
            self.amount
        )  # В объекте self._original_amount сохраняем сумму последнего платежа

    # Переопределяем метод save для обновления суммы сбора при создании нового платежа или изменении прежнего платежа
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Проверка на создание нового платежа (есть ли id)
        super().save(
            *args, **kwargs
        )  # Вызываем метод родительского класса и сохраняем в БД платеж
        # Обновляем сумму сбора при создании нового платежа
        if is_new:
            # Атомарно увеличиваем поле суммы сбора без явного сохранения объекта (так как всё происходит на уровне БД)
            # collect_id (id связанного объекта сбора collect) будет доступен, так как объект уже был сохранён
            Collect.objects.filter(pk=self.collect_id).update(
                collected_amount=F("collected_amount") + self.amount
            )
        else:
            # Существующий платёж: корректируем сумму сбора по разнице между прежним и текущим значением платежа
            if self._original_amount != self.amount:
                delta = self.amount - self._original_amount
                Collect.objects.filter(pk=self.collect_id).update(
                    collected_amount=F("collected_amount") + delta
                )
        self._original_amount = (
            self.amount
        )  # Обновляем прежнее значение платежа на текущее
