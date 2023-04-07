CREATE TABLE departamento (
  id INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY (id)
);

CREATE TABLE funcionario (
  id INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL UNIQUE,
  cpf VARCHAR(11) NOT NULL UNIQUE,
  rg VARCHAR(9) NOT NULL UNIQUE,
  sexo CHAR(1),
  data_nascimento DATE,
  habilitacao BOOLEAN,
  salario DECIMAL(10,2),
  carga_horaria_semanal DECIMAL(4,2),
  departamento_id INT,
  PRIMARY KEY (id),
  FOREIGN KEY (departamento_id) REFERENCES departamento(id)
);

CREATE TABLE projeto (
  id INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL,
  horas_necessarias INT,
  prazo_estimado DATE,
  horas_realizadas INT,
  ultimo_calculo_horas DATE,
  supervisor_id INT,
  departamento_id INT,
  PRIMARY KEY (id),
  FOREIGN KEY (supervisor_id) REFERENCES funcionario(id),
  FOREIGN KEY (departamento_id) REFERENCES departamento(id)
);

CREATE TABLE projeto_funcionario (
  projeto_id INT,
  funcionario_id INT,
  carga_horaria_semanal DECIMAL(4,2),
  PRIMARY KEY (projeto_id, funcionario_id),
  FOREIGN KEY (projeto_id) REFERENCES projeto(id),
  FOREIGN KEY (funcionario_id) REFERENCES funcionario(id)
);

ALTER TABLE projeto
ADD CONSTRAINT UQ_projeto_nome_departamento UNIQUE (nome, departamento_id);

