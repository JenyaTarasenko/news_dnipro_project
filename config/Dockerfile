# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем зависимости для PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Указываем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY config/requirements.txt /app/


# Добавьте статические файлы в контейнер
# COPY ./staticfiles /app/staticfiles


# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/
# Запуск команды collectstatic
RUN python manage.py collectstatic --noinput

# Открываем порт 8000 для внешнего доступа
EXPOSE 8000

# Команда для запуска сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
