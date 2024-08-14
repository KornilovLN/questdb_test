# Используем официальный образ QuestDB
FROM questdb/questdb:latest

# Устанавливаем необходимые зависимости (если нужно)
RUN apt-get update && apt-get install -y curl

# Устанавливаем переменные окружения для QuestDB
ENV QDB_ROOT=/var/lib/questdb
ENV PATH=$QDB_ROOT/bin:$PATH


