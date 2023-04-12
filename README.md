# CAM Admin
Projeto de gerenciamento de registros de departamentos, funcionários e projetos.

## Tecnologias utilizadas:
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green"/>
<img src="https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/>
<img src="https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white"/> </br>
Python 3.1 </br>
Django 4.2 </br>
Django Rest 3.14.0 </br>
MySQL 8 </br>
Docker-Compose 3.7 </br>
django-mysql 4.9.0 </br>
django_extensions 3.2.1 </br>
whitenoise 6.4.0 </br>

## Executando o projeto via Docker 🐋
Certifique-se de ter o Docker e o docker-compose instalados em sua máquina.
Clone o repositório e navegue até a pasta do projeto (provavelmente './django-cam'), </br> onde contém os diretórios 'backend.admin' e 'backend.mysql'.
Execute o comando:
> docker-compose up -d --build
>
para iniciar os containers '<strong>cam-admin</strong>' e '<strong>cam-mysqldb</strong>'.
### Acesse o projeto em http://localhost:8081/admin.
✅

## Storage Procedures
Há a possibilidade de utilizar procedures que realizam ações CRUD a partir de uma estrutura JSON. </br>
Primeiro é necessário criar as funções na base com o script em <strong>/backend.mysql/apply-procedures.sh</strong>:
> ./apply-procedures.sh
>
Há um exemplo de estrutura para inserção em: <strong>/backend.mysql/sqls/exemplo_insert_json.sql</strong>.

## Executando o projeto sem Docker 🔌
Certifique-se de ter o Python 3.1 e o MySQL 8 instalados em sua máquina. </br>
Clone o repositório e navegue até a pasta do projeto. </br>
Execute o comando para instalar as dependências do projeto:
> pip install -r requirements.txt
>
Execute o comando para criar e então aplicar as migrações do banco de dados:
> python manage.py makemigrations
>
> python manage.py migrate
>
Execute o comando para criar um usuário administrador:
> python manage.py createsuperuser
>
Execute o comando para iniciar o servidor local:
> python manage.py runserver
>
Acesse o projeto em http://localhost:8000 ou http://localhost:8081/admin (dependendo da port utilizada).

## Testes
Para executar os testes unitários, execute o comando:
> python manage.py test
>

## Diagrama da base de dados
<p align="center">
    <img width="460" height="200" src="backend.admin/resources/database_diag.png" alt="Diagrama da base de dados">
</p>
