# Используем официальный образ Python 3
FROM python:3.9-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем QuestDB
RUN curl -LO https://github.com/questdb/questdb/releases/download/6.0.5/questdb-6.0.5-rt-linux-amd64.tar.gz && \
    tar -xzf questdb-6.0.5-rt-linux-amd64.tar.gz && \
    mv questdb-6.0.5-rt-linux-amd64 /opt/questdb

# Устанавливаем необходимые Python пакеты
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипты в контейнер
COPY . /app
WORKDIR /app

# Устанавливаем переменные окружения для QuestDB
#ENV QDB_ROOT=/opt/questdb
#ENV PATH=$QDB_ROOT/bin:$PATH

# Устанавливаем точку входа
ENTRYPOINT ["/bin/bash"]

