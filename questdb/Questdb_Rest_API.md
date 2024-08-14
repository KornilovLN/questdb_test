## Работа с SQL запросами в questdb

### <<< Create Table >>>; <<< Insert a row >>> 
**_With cURL_**
```
# Create Table
curl -G \
  --data-urlencode "query=CREATE TABLE IF NOT EXISTS txt_data(timestamp TIMESTAMP, temperature DOUBLE, humidity INT)" \
  http://localhost:9000/exec
```
```
# Insert a row
curl -G \
  --data-urlencode "query=INSERT INTO txt_data VALUES(1633072800, 23.5, 56)" \
  http://localhost:9000/exec
```

```
# Select from ...
curl -G   --data-urlencode "query=SELECT * FROM txt_data;"   http://localhost:9000/exec
```

**_With python_**
```
import sys
import requests
import json

host = 'http://localhost:9000'

def run_query(sql_query):
    query_params = {'query': sql_query, 'fmt' : 'json'}
    try:
        response = requests.get(host + '/exec', params=query_params)
        json_response = json.loads(response.text)
        print(json_response)
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}', file=sys.stderr)

# create table
run_query("CREATE TABLE IF NOT EXISTS trades (timestamp TIMESTAMP, temperature DOUBLE, humidity INT)")

# insert row
run_query("INSERT INTO trades VALUES(1633072800, 23.5, 56)")
```

```
import sys
import requests

host = 'http://localhost:9000'

sql_query = "select * from txt_data"

try:
    response = requests.get(
        host + '/exec',
        params={'query': sql_query}).json()
    for row in response['dataset']:
        print(row[0])
except requests.exceptions.RequestException as e:
    print(f'Error: {e}', file=sys.stderr)
```





### <<< Select * from >>>
