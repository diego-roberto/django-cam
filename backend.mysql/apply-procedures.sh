#!/bin/bash

echo "Executando script..."
docker exec -i cam-mysqldb mysql -h127.0.0.1 -uroot -psecret < ./sqls/procedures.sql

exit 1
