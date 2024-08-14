## Работа questdb независимо от приложений
```
В данном случае надо создать официальный докер контейнер с questdb 
и запустить для возможности его использования подключаемыми модулями.
```

#### Формат таблиц

**_Текстовый формат_**
<br>В текстовом формате данные обычно передаются в виде строк,
<br>например, в формате CSV или JSON.

<br>Пример таблицы, создаваемой посредством SQL запроса:
```
run_query("CREATE TABLE IF NOT EXISTS txt_data (client STRING,
                                                timestamp TIMESTAMP,
                                                temperature INT,
                                                humidity INT)")
```

**_Как генерировать данные и создав таблицу в базе, писать в нее записи_**

```
#!/usr/bin/env python3

import sys
import requests
import json
import time
import random
import math
import argparse

PAUSE_MS = 1        # Пауза в миллисекундах
MAXCOUNT = 1000   

host = 'http://localhost:9000'

def run_query(sql_query):
    query_params = {'query': sql_query, 'fmt': 'json'}
    try:
        response = requests.get(host + '/exec', params=query_params)
        json_response = json.loads(response.text)
        #print(json_response)

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}', file=sys.stderr)


def generate_data(i):
    # Используем синусоиду для основной вариации
    t = 25.0 + 12.0 * math.sin(i / 100.0)         # Основная температура с синусоидальным изменением
    h = 50 + 20 * math.cos(i / 100.0)             # Основная влажность с косинусоидальным изменением

    # Добавляем случайные возмущения
    temperature = t + random.uniform(-0.5, 0.5)    # Небольшие случайные возмущения для температуры
    humidity = h + random.randint(-2, 2)           # Небольшие случайные возмущения для влажности
    return temperature, humidity


def main(client_name):
    global timestamp

    # Create table
    run_query("CREATE TABLE IF NOT EXISTS txt_data (client STRING, timestamp TIMESTAMP, temperature INT, humidity INT)")

    # Получаем текущее время в миллисекундах
    starttime = int(time.time() * 1000)
    timestamp = starttime
    
    for i in range(0, MAXCOUNT):

        temperature, humidity = generate_data(i)

        # Вставка строки с именем клиента
        query = f"INSERT INTO txt_data (client, timestamp, temperature, humidity) VALUES ('{client_name}', {timestamp}, {temperature}, {humidity})"
        run_query(query)

        # Пауза в миллисекундах
        time.sleep(PAUSE_MS / 1000.0)   # time.sleep принимает значение в секундах
        timestamp += PAUSE_MS  

    endtime = int(time.time() * 1000)    
    print("elapsed time (ms): ", endtime - starttime)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Insert data into the database with client name.')
    parser.add_argument('--name', required=True, help='Client name to identify the data source.')
    args = parser.parse_args()
    
    main(args.name)
```

**_Проведение теста обращения к таблице базы из 10-ти приложений одновременно_**
<br>Для этого нужен скрипт, чтобы запустить все приложения почти одновременно.
<br>В данном случае нужно запустить 10 приложений, которые будут постоянно вставлять данные в базу.

- #!/bin/bash
- CLIENTS=("client_1" "client_2" "client_3" "client_4" "client_5" "client_6" "client_7" "client_8" "client_9" "client_10")
- echo "Start 10 clients write to txt_data DB"
- for client in "${CLIENTS[@]}"; do
-     xterm -e "/mnt/poligon/questdb_test/questdb/inserter.py --name $client; exec bash" &
- done

**_Выводы_**
<br>Этот тест позволит вам засечь время, затраченное на отправку данных в текстовом формате.


#### Для создания базы данных и таблиц в проекте применим питоновское приложение,
<br>для реализации необходимых функций
* для наполнения,
* чтения и
* отображения данных,
<br>можно использовать базу данных временных рядов, такую как QuestDB.
<br>QuestDB поддерживает как текстовый, так и бинарный формат данных.

**_Шаги для реализации:_**

* Создание базы данных и таблиц.
* Наполнение таблиц данными.
* Чтение из таблицы и отображение на дисплее хоста.

1. Создание базы данных и таблиц
<br>Для создания базы данных и таблиц в QuestDB можно использовать SQL-запросы.
<br>В этом примере мы создадим две таблицы: одну для текстового формата и одну для бинарного.

<br>Пример SQL-запросов для создания таблиц:
```
CREATE TABLE text_data (
    client STRING,
    timestamp TIMESTAMP,
    temperature INT,
    humidity INT
);
```

2. Наполнение таблиц данными
<br>Для наполнения таблиц данными можно использовать Python и библиотеку requests для отправки данных в QuestDB.
<br>Ввше приведен код


3. Чтение данных в массив структур
<br>Для чтения данных из таблиц можно использовать SQL-запросы и библиотеку requests для получения данных из QuestDB.

<br>Пример кода для чтения данных:
```
#!/usr/bin/env python3

import sys
import requests
import time

host = 'http://localhost:9000'

sql_query = "select * from txt_data"

starttime = int(time.time() * 1000)

counter = 0

try:
    response = requests.get(
        host + '/exec',
        params={'query': sql_query}).json()

    responsetime = int(time.time() * 1000) - starttime

    for row in response['dataset']:
        print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")
        counter += 1

except requests.exceptions.RequestException as e:
    print(f'Error: {e}', file=sys.stderr)

print("responsetime (ms): ", responsetime)

elapsedtime = int(time.time() * 1000) - starttime
print("elapsedtime (ms): ", elapsedtime)
print("counter: ", counter)
```

#### Удобство просмотра результатов работы приложений

**_Открыть в браузере  localhost:9000_**
<br>В web приложении questdb предоставляет возможности:
* Вручную писать SQL запросы для создания, наполнения, чтения и удаления таблиц
* Проверять данные, что пришли извне также с пом. SQL запросов
* Выводить данные в табличной форме и графиками 
* Получать выборки любой сложности
