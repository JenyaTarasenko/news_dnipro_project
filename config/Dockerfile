# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем зависимости для PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем виртуальное окружение и активируем его
RUN python -m venv venv
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Запуск команды collectstatic
RUN ./venv/bin/python manage.py collectstatic --noinput 

# Открываем порт 8000 для внешнего доступа
EXPOSE 8000

# Команда для запуска сервера Django с использованием gunicorn
CMD ["./venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
