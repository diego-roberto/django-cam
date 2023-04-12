#!/bin/bash

echo "Executando script..."
docker exec -i cam-mysqldb mysql -h127.0.0.1 -uroot -ptopsecret < ./sqls/procedures.sql

exit 1
