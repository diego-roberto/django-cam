UPDATE mysql.db SET User = 'root' WHERE Host = '%' AND Db = 'empresa' AND User = 'cam_usr';

GRANT ALL PRIVILEGES ON empresa.* TO 'root'@'%';

FLUSH PRIVILEGES;

## resto do script:
## aqui
