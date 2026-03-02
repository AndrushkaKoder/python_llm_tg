FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей из корня проекта
# (учитывая, что контекст сборки может быть разным, лучше копировать точечно)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код (папку src и т.д.)
COPY . .

# Отключаем буферизацию логов (чтобы сразу видеть вывод в docker logs)
ENV PYTHONUNBUFFERED=1

# Запускаем приложение
CMD ["python", "-m", "src.main.py"]
