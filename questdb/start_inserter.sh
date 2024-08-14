#!/bin/bash

CLIENTS=("client_1" "client_2" "client_3" "client_4" "client_5" "client_6" "client_7" "client_8" "client_9" "client_10")

echo "Start 10 clients write to txt_data DB"

for client in "${CLIENTS[@]}"; do
    xterm -e "/mnt/poligon/questdb_test/questdb/inserter.py --name $client; exec bash" &
done


