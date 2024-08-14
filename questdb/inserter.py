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

