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

