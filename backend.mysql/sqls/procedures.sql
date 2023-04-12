USE empresa;

-- INICIO da Criação das Storage Procedures
DELIMITER $$

-- funcionario
CREATE PROCEDURE sp_insert_funcionario(IN json_str JSON)
BEGIN
SET @nome = JSON_EXTRACT(json_str, '$.nome');
SET @cpf = JSON_EXTRACT(json_str, '$.cpf');
SET @rg = JSON_EXTRACT(json_str, '$.rg');
SET @sexo = JSON_EXTRACT(json_str, '$.sexo');
SET @data_nascimento = JSON_EXTRACT(json_str, '$.data_nascimento');
SET @habilitacao = JSON_EXTRACT(json_str, '$.habilitacao');
SET @salario = JSON_EXTRACT(json_str, '$.salario');
SET @carga_horaria = JSON_EXTRACT(json_str, '$.carga_horaria');
SET @departamento_id = JSON_EXTRACT(json_str, '$.departamento_id');

INSERT INTO funcionario (nome, cpf, rg, sexo, data_nascimento, habilitacao, salario, carga_horaria, departamento_id)
VALUES (@nome, @cpf, @rg, @sexo, @data_nascimento, @habilitacao, @salario, @carga_horaria, @departamento_id);
END$$

CREATE PROCEDURE sp_select_all_funcionario()
BEGIN
SELECT * FROM funcionario;
END$$

CREATE PROCEDURE sp_select_funcionario_by_id(IN func_id INT)
BEGIN
SELECT * FROM funcionario WHERE id = func_id;
END$$

CREATE PROCEDURE sp_update_funcionario(IN func_id INT, IN func_data JSON)
BEGIN
UPDATE funcionario SET
nome = JSON_EXTRACT(func_data, "$.nome"),
cpf = JSON_EXTRACT(func_data, "$.cpf"),
rg = JSON_EXTRACT(func_data, "$.rg"),
sexo = JSON_EXTRACT(func_data, "$.sexo"),
data_nascimento = JSON_EXTRACT(func_data, "$.data_nascimento"),
habilitacao = JSON_EXTRACT(func_data, "$.habilitacao"),
salario = JSON_EXTRACT(func_data, "$.salario"),
carga_horaria = JSON_EXTRACT(func_data, "$.carga_horaria"),
departamento_id = JSON_EXTRACT(func_data, "$.departamento_id")
WHERE id = func_id;
END$$

CREATE PROCEDURE sp_delete_funcionario_by_id(IN func_id INT)
BEGIN
DELETE FROM funcionario WHERE id = func_id;
END$$

-- departamento
CREATE PROCEDURE sp_insert_departamento(IN json_str JSON)
BEGIN
SET @nome = JSON_EXTRACT(json_str, '$.nome');

INSERT INTO departamento (nome)
VALUES (@nome);
END$$

CREATE PROCEDURE sp_select_departamento(IN dep_id INT)
BEGIN
SELECT * FROM departamento WHERE id = dep_id;
END$$

CREATE PROCEDURE sp_update_departamento(IN dep_id INT, IN json_str JSON)
BEGIN
SET @nome = JSON_EXTRACT(json_str, '$.nome');

UPDATE departamento SET
nome = @nome
WHERE id = dep_id;
END$$

CREATE PROCEDURE sp_delete_departamento(IN dep_id INT)
BEGIN
DELETE FROM departamento WHERE id = dep_id;
END$$

-- projeto
CREATE PROCEDURE sp_insert_projeto(IN json_data JSON)
BEGIN
  SET @nome = JSON_EXTRACT(json_data, '$.nome');
  SET @horas_necessarias = JSON_EXTRACT(json_data, '$.horas_necessarias');
  SET @prazo_estimado = JSON_EXTRACT(json_data, '$.prazo_estimado');
  SET @supervisor_id = JSON_EXTRACT(json_data, '$.supervisor_id');
  SET @departamento_id = JSON_EXTRACT(json_data, '$.departamento_id');

INSERT INTO projeto (nome, horas_necessarias, prazo_estimado, supervisor_id, departamento_id)
  VALUES (@nome, @horas_necessarias, @prazo_estimado, @supervisor_id, @departamento_id);
END$$

CREATE PROCEDURE sp_select_projeto_by_id(IN proj_id INT)
BEGIN
SELECT * FROM projeto WHERE id = proj_id;
END$$

CREATE PROCEDURE sp_update_projeto(IN proj_id INT, IN json_data JSON)
BEGIN
UPDATE projeto SET
    nome = JSON_EXTRACT(json_data, '$.nome'),
    horas_necessarias = JSON_EXTRACT(json_data, '$.horas_necessarias'),
    prazo_estimado = JSON_EXTRACT(json_data, '$.prazo_estimado'),
    supervisor_id = JSON_EXTRACT(json_data, '$.supervisor_id'),
    departamento_id = JSON_EXTRACT(json_data, '$.departamento_id')
WHERE id = proj_id;
END$$

CREATE PROCEDURE sp_delete_projeto(IN proj_id INT)
BEGIN
DELETE FROM projeto WHERE id = proj_id;
END$$

-- projeto_funcionario
CREATE PROCEDURE sp_insert_projeto_funcionario(
IN projeto_id INT,
IN funcionario_id INT,
IN carga_horaria_semanal INT
)
BEGIN
INSERT INTO projeto_funcionario (projeto_id, funcionario_id, carga_horaria_semanal)
VALUES (projeto_id, funcionario_id, carga_horaria_semanal);
END$$

CREATE PROCEDURE sp_update_projeto_funcionario(
IN projeto_id INT,
IN funcionario_id INT,
IN carga_horaria_semanal INT
)
BEGIN
UPDATE projeto_funcionario
SET carga_horaria_semanal = carga_horaria_semanal
WHERE projeto_id = projeto_id AND funcionario_id = funcionario_id;
END$$

CREATE PROCEDURE sp_delete_projeto_funcionario(
IN projeto_id INT,
IN funcionario_id INT
)
BEGIN
DELETE FROM projeto_funcionario
WHERE projeto_id = projeto_id AND funcionario_id = funcionario_id;
END$$

CREATE PROCEDURE sp_select_projeto_funcionario(IN projeto_id INT)
BEGIN
SELECT pf.projeto_id, pf.funcionario_id, pf.carga_horaria_semanal,
p.nome as nome_projeto, f.nome as nome_funcionario
FROM projeto_funcionario pf
JOIN projeto p ON pf.projeto_id = p.id
JOIN funcionario f ON pf.funcionario_id = f.id
WHERE pf.projeto_id = projeto_id;
END$$

-- FIM da Criação das Storage Procedures

DELIMITER ;

