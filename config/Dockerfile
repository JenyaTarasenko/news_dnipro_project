# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем зависимости для PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Указываем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Добавляем WhiteNoise для статических файлов
# Убедитесь, что WhiteNoise добавлен в requirements.txt
# Убедитесь, что в settings.py у вас настроен WhiteNoise
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Запуск команды collectstatic
RUN python manage.py collectstatic --noinput 

# Открываем порт 8000 для внешнего доступа
EXPOSE 8000

# Команда для запуска сервера Django
# Лучше использовать gunicorn для продакшн-окружения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
