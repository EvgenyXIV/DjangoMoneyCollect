import os
from dotenv import load_dotenv

import os
from pathlib import Path

from decouple import Config, RepositoryEnv # импортируем модуль для работы с переменными окружения

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)

config = Config(RepositoryEnv(r'C:/Users/EvgenyMINI_S/PythonProjects/DjangoMoneyCollect/.env.dev'))
print(config('EMAIL_USER'))  # Должно вывести полный email-адрес
# print(config)
