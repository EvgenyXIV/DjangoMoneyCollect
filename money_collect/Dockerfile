# Базовый образ для Python
# https://hub.docker.com/_/python
FROM python:3.12-slim

# Создаём группу и пользователя для запуска Celery от имени непривилегированного пользователя
RUN if ! getent group celerygroup >/dev/null; then groupadd -r celerygroup; fi
RUN if ! getent passwd celeryuser >/dev/null; then useradd -m -r -g celerygroup celeryuser; fi

# Устанавливаем рабочую директорию (после этого "." или "/money_collect"- адреса рабочей директории в контейнере)
WORKDIR /usr/src/money_collect/

# файлы .pyc могут содержать чувствительную информацию, 
# и их включение в образ может быть нежелательным.
# Запрещаем их копирование
ENV PYTHONDONTWRITEBYTECODE=1

# Запрещаем вывод stdout stderr вместо их настройки для логирования
# Так меньше ошибок и нет риска потери данных при удалении контейнера
ENV PYTHONUNBUFFERED=1

# Устанавливаем системные зависимости (curl, postgresql-client)
RUN apt-get update && \
    apt-get install -y \
    curl \
    postgresql-client

# Устанавливаем Python зависимости
# Сначала копируем requirements.txt в рабочую директорию для кэширования
COPY ./requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip

# Параметр --no-cache-dir не указываем, кэширование (происходит по умолчанию) требуется.
# Это предохраняет от скачивания и установки обновлённых пакетов из репозитория,
# что может привести к проблемам с зависимостями.
RUN pip install -r requirements.txt



# Копирование файла скрипта из текущей папки проекта в рабочую папку контейнера для подключения к базе данных
# и созданию структуры БД по миграциям
COPY ./entrypoint.sh .


# На всякий случай, если в редакторе Windows изменялся файл, 
# то удаляем символы возврата каретки "\r" в конце строк для совместимости формата файла с Linux.
# Удаление знаков возврата каретки "\r" в конце строк (в среде windows \r\n, в Linux толко \n).
# Конвертация формата EOL (Windows -> Linux)
# Get-Content — читает содержимое файла
# Foreach-Object — обрабатывает каждую строку
# -replace — заменяет символы
# Set-Content — записывает изменённое содержимое обратно
# в среде Linux для совместимости после правки в Windows
RUN sed -i 's/\r$//g' /usr/src/money_collect/entrypoint.sh

# Даём право запуска файла entrypoint.sh на исполнение в среде Docker-desctop (Unix)
RUN chmod +x /usr/src/money_collect/entrypoint.sh

# Копируем все файлы проекта из текущей папки на диске в рабочую директорию контейнера
COPY . .

# Установка разрешений на рабочий каталог-Переключение на пользователя celeryuser-Запуск Celery worker
RUN chown -R celeryuser:celerygroup /usr/src/money_collect
USER celeryuser
CMD ["celery", "-A", "money_collect", "worker", "-l", "info", "-P", "gevent"]

# Установка точки входа для запуска контейнера в файле entrypoint.sh
ENTRYPOINT ["/usr/src/money_collect/entrypoint.sh"]
