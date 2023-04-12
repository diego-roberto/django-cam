CREATE DATABASE IF NOT EXISTS empresa;

USE empresa;

CREATE TABLE departamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) UNIQUE
);

CREATE TABLE funcionario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) UNIQUE,
    cpf CHAR(11) UNIQUE,
    rg CHAR(9) UNIQUE,
    sexo CHAR(1),
    data_nascimento DATE,
    habilitacao BOOLEAN,
    salario DECIMAL(10, 2),
    carga_horaria_semanal SMALLINT UNSIGNED,
    is_supervisor BOOLEAN DEFAULT FALSE,
    departamento_id INT,
    FOREIGN KEY (departamento_id) REFERENCES departamento(id)
);

CREATE TABLE projeto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) UNIQUE,
    horas_necessarias INT UNSIGNED,
    prazo_estimado DATE,
    horas_realizadas INT UNSIGNED DEFAULT 0,
    carga_horaria_total INT UNSIGNED DEFAULT 0,
    ultimo_calculo_horas DATE,
    departamento_id INT,
    supervisor_id INT,
    FOREIGN KEY (departamento_id) REFERENCES departamento(id),
    FOREIGN KEY (supervisor_id) REFERENCES funcionario(id)
);

CREATE TABLE projeto_funcionario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    projeto_id INT,
    funcionario_id INT,
    funcao CHAR(1),
    carga_horaria_semanal SMALLINT UNSIGNED DEFAULT 0,
    FOREIGN KEY (projeto_id) REFERENCES projeto(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionario(id),
    UNIQUE (projeto_id, funcionario_id)
);

CREATE INDEX idx_funcionario_departamento ON funcionario (departamento_id);
CREATE INDEX idx_projeto_departamento ON projeto (departamento_id);
CREATE INDEX idx_projeto_supervisor ON projeto (supervisor_id);
CREATE INDEX idx_projeto_funcionario_projeto ON projeto_funcionario (projeto_id);
CREATE INDEX idx_projeto_funcionario_funcionario ON projeto_funcionario (funcionario_id);

ALTER TABLE projeto
ADD CONSTRAINT UQ_projeto_nome_departamento UNIQUE (nome, departamento_id);

