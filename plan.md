## Сравнительный тест работы в questdb с данными в текстовом и бинарном виде
```
Работа с бинарным форматом данных в схеме использования баз данных временных рядов
может значительно повысить производительность и уменьшить объем передаваемых данных.
Давайте рассмотрим, как можно работать с бинарным форматом данных в приложении на Python
и как можно построить сравнительный тест для перемещения
сгенерированных данных в базу данных временных рядов (например, QuestDB) двумя способами: текстовым и бинарным.
```

#### Форматы пакетов

**_Текстовый формат_**
<br>В текстовом формате данные обычно передаются в виде строк,
<br>например, в формате CSV или JSON.

<br>Пример строки в формате CSV:
```
timestamp,temperature,humidity
2023-10-01T12:00:00Z,22.5,60
2023-10-01T12:01:00Z,22.6,61
```

**_Бинарный формат_**
<br>В бинарном формате данные кодируются в виде байтов,
<br>что позволяет уменьшить объем передаваемых данных и ускорить их обработку.
<br>Пример бинарного формата может включать использование struct в Python, для упаковки данных.

<br>Пример использования struct для упаковки данных:
```
import struct

# Пример данных
timestamp = 1633072800  # Unix timestamp
temperature = 22.5
humidity = 60

# Упаковка данных в бинарный формат
binary_data = struct.pack('!IfI', timestamp, temperature, humidity)
```

**_Сравнительный тест_**
<br>Для проведения сравнительного теста нам нужно:
* Сгенерировать данные.
* Отправить данные в базу данных двумя способами: текстовым и бинарным.
* Измерить время и объем переданных данных.

```
#Генерация данных
import time
import random

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

#Отправка данных в текстовом формате
import requests
import json

def send_text_data(data):
    url = 'http://localhost:9000/insert'  # URL для вставки данных в QuestDB
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    response = requests.post(url, headers=headers, data=json_data)
    return response.status_code

#Отправка данных в бинарном формате
import struct

def send_binary_data(data):
    url = 'http://localhost:9000/insert'  # URL для вставки данных в QuestDB
    headers = {'Content-Type': 'application/octet-stream'}
    binary_data = b''
    for record in data:
        binary_data += struct.pack('!IfI', record['timestamp'], record['temperature'], record['humidity'])
    response = requests.post(url, headers=headers, data=binary_data)
    return response.status_code
```

**_Проведение теста_**
```
import time

# Генерация данных
num_records = 1000
data = generate_data(num_records)

# Тестирование текстового формата
start_time = time.time()
send_text_data(data)
text_duration = time.time() - start_time

# Тестирование бинарного формата
start_time = time.time()
send_binary_data(data)
binary_duration = time.time() - start_time

print(f'Text format duration: {text_duration} seconds')
print(f'Binary format duration: {binary_duration} seconds')
```

**_Выводы_**
<br>Этот тест позволит вам сравнить время, затраченное на отправку данных в текстовом и бинарном форматах.
<br>Обычно бинарный формат будет более эффективным с точки зрения объема передаваемых данных и времени передачи,
<br>особенно при работе с большими объемами данных.

#### Форматы пакетов

**_Текстовый формат Формат: JSON или CSV_**
<br>Пример JSON:
```[
  {"timestamp": 1633072800, "temperature": 22.5, "humidity": 60},
  {"timestamp": 1633072860, "temperature": 22.6, "humidity": 61}
]
```

**_Бинарный формат_**
<br>Формат: Упакованные байты с использованием struct
<br>Пример упаковки:
```
struct.pack('!IfI', timestamp, temperature, humidity)
```

#### Для создания базы данных и двух таблиц в проекте,
<br>а также для реализации необходимых функций
* для наполнения,
* чтения и
* отображения данных,
<br>можно использовать базу данных временных рядов, такую как QuestDB.
<br>QuestDB поддерживает как текстовый, так и бинарный формат данных.

**_Шаги для реализации:_**

* Создание базы данных и таблиц.
* Наполнение таблиц данными.
* Чтение данных в массив структур.
* Чтение из массива и отображение на дисплее хоста.

1. Создание базы данных и таблиц
<br>Для создания базы данных и таблиц в QuestDB можно использовать SQL-запросы.
<br>В этом примере мы создадим две таблицы: одну для текстового формата и одну для бинарного.

<br>Пример SQL-запросов для создания таблиц:
```
CREATE TABLE text_data (
    timestamp TIMESTAMP,
    temperature DOUBLE,
    humidity INT
);
```
```
CREATE TABLE binary_data (
    timestamp TIMESTAMP,
    temperature DOUBLE,
    humidity INT
);
```

2. Наполнение таблиц данными
<br>Для наполнения таблиц данными можно использовать Python и библиотеку requests для отправки данных в QuestDB.

<br>Пример кода для наполнения таблиц:
```
import time
import random
import requests
import struct

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
    url = 'http://localhost:9000/exec'  # URL для вставки данных в QuestDB
    headers = {'Content-Type': 'application/json'}
    for record in data:
        json_data = {
            'query': f"INSERT INTO text_data VALUES('{record['timestamp']}', {record['temperature']}, {record['humidity']})"
        }
        response = requests.post(url, headers=headers, json=json_data)
        if response.status_code != 200:
            print(f"Error inserting data: {response.text}")

# Отправка данных в бинарном формате
def send_binary_data(data):
    url = 'http://localhost:9000/exec'  # URL для вставки данных в QuestDB
    headers = {'Content-Type': 'application/octet-stream'}
    binary_data = b''
    for record in data:
        binary_data += struct.pack('!IfI', record['timestamp'], record['temperature'], record['humidity'])
    response = requests.post(url, headers=headers, data=binary_data)
    if response.status_code != 200:
        print(f"Error inserting data: {response.text}")

# Генерация и отправка данных
num_records = 10000
data = generate_data(num_records)
send_text_data(data)
send_binary_data(data)
```

3. Чтение данных в массив структур
<br>Для чтения данных из таблиц можно использовать SQL-запросы и библиотеку requests для получения данных из QuestDB.

<br>Пример кода для чтения данных:
```
import requests

# Чтение данных из таблицы text_data
def read_text_data():
    url = 'http://localhost:9000/exec'  # URL для выполнения запросов в QuestDB
    query = "SELECT * FROM text_data"
    response = requests.get(url, params={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error reading data: {response.text}")
        return []

# Чтение данных из таблицы binary_data
def read_binary_data():
    url = 'http://localhost:9000/exec'  # URL для выполнения запросов в QuestDB
    query = "SELECT * FROM binary_data"
    response = requests.get(url, params={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error reading data: {response.text}")
        return []

# Чтение данных
text_data = read_text_data()
binary_data = read_binary_data()
```

4. Чтение из массива и отображение на дисплее хоста
<br>Для отображения данных на дисплее хоста можно использовать стандартный вывод в консоль.

<br>Пример кода для отображения данных:
```
# Отображение данных
def display_data(data):
    for record in data:
        print(f"Timestamp: {record['timestamp']}, Temperature: {record['temperature']}, Humidity: {record['humidity']}")

# Отображение данных из text_data
print("Text Data:")
display_data(text_data)

# Отображение данных из binary_data
print("Binary Data:")
display_data(binary_data)
```


#--------------------------------------------------------------------------------------
Полный пример
#--------------------------------------------------------------------------------------
```
import time
import random
import requests
import struct

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
    url = 'http://localhost:9000/exec'  # URL для вставки данных в QuestDB
    headers = {'Content-Type': 'application/json'}
    for record in data:
        json_data = {
            'query': f"INSERT INTO text_data VALUES('{record['timestamp']}', {record['temperature']}, {record['humidity']})"
        }
        response = requests.post(url, headers=headers, json=json_data)
        if response.status_code != 200:
            print(f"Error inserting data: {response.text}")

# Отправка данных в бинарном формате
def send_binary_data(data):
    url = 'http://localhost:9000/exec'  # URL для вставки данных в QuestDB
    headers = {'Content-Type': 'application/octet-stream'}
    binary_data = b''
    for record in data:
        binary_data += struct.pack('!IfI', record['timestamp'], record['temperature'], record['humidity'])
    response = requests.post(url, headers=headers, data=binary_data)
    if response.status_code != 200:
        print(f"Error inserting data: {response.text}")

# Чтение данных из таблицы text_data
def read_text_data():
    url = 'http://localhost:9000/exec'  # URL для выполнения запросов в QuestDB
    query = "SELECT * FROM text_data"
    response = requests.get(url, params={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error reading data: {response.text}")
        return []

# Чтение данных из таблицы binary_data
def read_binary_data():
    url = 'http://localhost:9000/exec'  # URL для выполнения запросов в QuestDB
    query = "SELECT * FROM binary_data"
    response = requests.get(url, params={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error reading data: {response.text}")
        return []

# Отображение данных
def display_data(data):
    for record in data:
        print(f"Timestamp: {record['timestamp']}, Temperature: {record['temperature']}, Humidity: {record['humidity']}")

# Генерация и отправка данных
num_records = 10000
data = generate_data(num_records)
send_text_data(data)
send_binary_data(data)

# Чтение данных
text_data = read_text_data()
binary_data = read_binary_data()

# Отображение данных
print("Text Data:")
display_data(text_data)

print("Binary Data:")
display_data(binary_data)
```

Этот пример показывает:

* как создать базу данных и таблицы,
* наполнить их данными,
* прочитать данные и
* отобразить их на дисплее хоста.


