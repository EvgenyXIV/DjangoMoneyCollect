import gevent.monkey

gevent.monkey.patch_all()  # ⚠️ Должно быть первым! Патчит все стандартные библиотеки.

from django.core.mail import (
    send_mail,
)  # Функция для отправки email, декорирующая упрощённое использование класса

# EmailMessage для более сложных сценариев
from smtplib import SMTPException

from django.template.loader import render_to_string  # Функция для рендера шаблона
from django.utils.html import strip_tags  # Функция для удаления html-тегов из текста

from money_collect.settings import (
    DEFAULT_FROM_EMAIL,
)  # Адрес отправителя из настроек settings.py
from api.models import Collect, Payment  # Модели сбора и платежа
from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver

from socket import gaierror  # Импортируем gaierror для обработки ошибок

from_email = DEFAULT_FROM_EMAIL  # Адрес отправителя из настроек settings.py
# Задачи для отправки уведомлений


# Декоратор для Celery для асинхронной отправки email (2 попытки с задержкой 2 секунды)
@shared_task(
    autoretry_for=(gaierror,), retry_kwargs={"max_retries": 2, "countdown": 2}
)  # Декоратор для Celery для асинхронной отправки email
def send_collect_created(
    collect_id,
):  # Функция для отправки уведомления, принимает id сбора
    collect = Collect.objects.get(pk=collect_id)  # Получение объекта сбора по id
    # Параметры для отправки email
    subject = "Collect created successfully"  # Тема письма
    message = render_to_string(
        "api/collect_created.txt", {"collect": collect}
    )  # Шаблон письма
    plain_message = strip_tags(message)  # Текст письма без html-тегов
    to_email = collect.author.email  # Получатель письма

    # Отправка письма с помощью встроенной функции send_mail
    try:
        send_mail(
            subject,
            plain_message,
            from_email,  # Отправитель из настроек settings.py
            [to_email],  # Cписок получателей
            html_message=message,  # HTML-версия письма с тегами (если требуется)
            fail_silently=False,  # Не отключать уведомление о неудаче
        )
        return True
    except SMTPException as e:
        print(f"Ошибка при отправке email: {str(e)}")
    return False


# Декоратор для Celery для асинхронной отправки email (2 попытки с задержкой 2 секунды)
@shared_task(autoretry_for=(gaierror,), retry_kwargs={"max_retries": 2, "countdown": 2})
def send_payment_created(payment_id):
    payment = Payment.objects.get(pk=payment_id)
    subject = "Payment made successfully"
    message = render_to_string(
        "api/payment_made.txt", {"payment": payment, "collect": payment.collect}
    )
    plain_message = strip_tags(message)
    to_email = payment.user.email
    # print(f"Отправка письма от {DEFAULT_FROM_EMAIL} на: {to_email}")  # Логирование email

    try:
        send_mail(
            subject,
            plain_message,
            from_email,
            [to_email],
            html_message=message,
            fail_silently=False,
        )
        print("Письмо отправлено успешно")  # Логирование успешной отправки email
        return True
    except SMTPException as e:
        print(f"Ошибка при отправке email: {str(e)}")
        return False


# Декоратор для Celery для асинхронной отправки email (2 попытки с задержкой 2 секунды)
@shared_task(autoretry_for=(gaierror,), retry_kwargs={"max_retries": 2, "countdown": 2})
def send_collect_updated(
    collect_id,
):  # Функция для отправки уведомления, принимает id сбора
    collect = Collect.objects.get(pk=collect_id)  # Получение объекта сбора по id
    # Параметры для отправки email
    subject = "Collect updated successfully"  # Тема письма
    message = render_to_string(
        "api/collect_updated.txt", {"collect": collect}
    )  # Шаблон письма
    plain_message = strip_tags(message)  # Текст письма без html-тегов
    to_email = collect.author.email  # Получатель письма

    # Отправка письма с помощью встроенной функции send_mail
    try:
        send_mail(
            subject,
            plain_message,
            from_email,  # Отправитель из настроек settings.py
            [to_email],  # Cписок получателей
            html_message=message,  # HTML-версия письма с тегами (если требуется)
            fail_silently=False,  # Не отключать уведомление о неудаче
        )
        return True
    except SMTPException as e:
        print(f"Ошибка при отправке email: {str(e)}")
    return False


# Декоратор для Celery для асинхронной отправки email (2 попытки с задержкой 2 секунды)
@shared_task(autoretry_for=(gaierror,), retry_kwargs={"max_retries": 2, "countdown": 2})
def send_payment_updated(payment_id):
    payment = Payment.objects.get(pk=payment_id)
    subject = "Payment updated successfully"
    message = render_to_string(
        "api/payment_updated.txt", {"payment": payment, "collect": payment.collect}
    )
    plain_message = strip_tags(message)
    to_email = payment.user.email
    # print(f"Отправка письма от {DEFAULT_FROM_EMAIL} на: {to_email}")  # Логирование email

    try:
        send_mail(
            subject,
            plain_message,
            from_email,
            [to_email],
            html_message=message,
            fail_silently=False,
        )
        print("Письмо отправлено успешно")  # Логирование успешной отправки email
        return True
    except SMTPException as e:
        print(f"Ошибка при отправке email: {str(e)}")
        return False


# Обработчики сигналов
@receiver(
    post_save, sender=Collect
)  # Декоратор для сигнала post_save для модели Collect
def trigger_notify_collect(
    sender, instance, created, **kwargs
):  # Обработчик сигнала, принимает экземпляр модели и флаг создания
    if created:
        send_collect_created.delay(
            instance.pk
        )  # Вызов задачи для отправки уведомления о создании сбора
    else:
        send_collect_updated.delay(
            instance.pk
        )  # Вызов задачи для отправки уведомления об обновлении сбора


@receiver(post_save, sender=Payment)
def trigger_notify_payment(sender, instance, created, **kwargs):
    if created:
        send_payment_created.delay(instance.pk)
    else:
        send_payment_updated.delay(instance.pk)
