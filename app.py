import time
import random
import requests
import struct
import sys

# URL для выполнения запросов в QuestDB
QUESTDB_URL = 'http://localhost:9000/exec'

# Функция для ожидания нажатия клавиши "a"
def wait_for_a():
    while True:
        user_input = input("Нажмите 'a' для продолжения: ")
        if user_input.lower() == 'a':
            break

# Создание таблиц
def create_tables():
    queries = [
        "CREATE TABLE IF NOT EXISTS text_data (timestamp TIMESTAMP, temperature DOUBLE, humidity INT);",
        "CREATE TABLE IF NOT EXISTS binary_data (timestamp TIMESTAMP, temperature DOUBLE, humidity INT);"
    ]
    headers = {'Content-Type': 'application/json'}
    for query in queries:
        json_data = {'query': query}
        response = requests.post(QUESTDB_URL, headers=headers, json=json_data)
        if response.status_code != 200:
            print(f"Ошибка создания таблиц: {response.text}")
        else:
            print(f"Таблица успешно создана или уже существует: {query}")

# Генерация данных
def generate_data(num_records):
    data = []
    current_time = int(time.time())
    for _ in range(num_records):
        record = {
            'timestamp': current_time,
            'temperature': round(random.uniform(20.0, 25.0), 2),
            'humidity': random.randint(50, 70)
        }
        data.append(record)
        current_time += 60  # Добавляем 1 минуту
    return data

# Отправка данных в текстовом формате
def send_text_data(data):
    headers = {'Content-Type': 'application/json'}
    for record in data:
        json_data = {
            'query': f"INSERT INTO text_data VALUES('{record['timestamp']}', {record['temperature']}, {record['humidity']})"
        }
        response = requests.post(QUESTDB_URL, headers=headers, json=json_data)
        if response.status_code != 200:
            print(f"Ошибка вставки данных: {response.text}")
        else:
            print(f"Данные успешно вставлены в text_data: {record}")
        while True:
            time.sleep(1)

# Отправка данных в бинарном формате
def send_binary_data(data):
    headers = {'Content-Type': 'application/octet-stream'}
    binary_data = b''
    for record in data:
        binary_data += struct.pack('!IfI', record['timestamp'], record['temperature'], record['humidity'])
    response = requests.post(QUESTDB_URL, headers=headers, data=binary_data)
    if response.status_code != 200:
        print(f"Ошибка вставки данных: {response.text}")
    else:
        print(f"Данные успешно вставлены в binary_data: {record}")

# Чтение данных из таблицы text_data
def read_text_data():
    query = "SELECT * FROM text_data"
    response = requests.get(QUESTDB_URL, params={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error reading data: {response.text}")
        return []

# Чтение данных из таблицы binary_data
def read_binary_data():
    query = "SELECT * FROM binary_data"
    response = requests.get(QUESTDB_URL, params={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error reading data: {response.text}")
        return []

# Отображение данных
def display_data(data):
    for record in data:
        print(f"Timestamp: {record['timestamp']}, Temperature: {record['temperature']}, Humidity: {record['humidity']}")

# Основная функция
def main():
    # Создание таблиц
    create_tables()

    wait_for_a()

    # Генерация и отправка данных
    num_records = 10000
    data = generate_data(num_records)

    wait_for_a()

    # Отправка данных
    send_text_data(data)
    send_binary_data(data)

    wait_for_a()

    # Чтение данных
    text_data = read_text_data()
    binary_data = read_binary_data()

    wait_for_a()

    # Отображение данных
    print("Text Data:")
    display_data(text_data)

    print("Binary Data:")
    display_data(binary_data)

if __name__ == "__main__":
    main()

