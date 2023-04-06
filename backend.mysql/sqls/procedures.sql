-- Alteração das permissões (se necessário):
UPDATE mysql.db SET User = 'root' WHERE Host = '%' AND Db = 'empresa' AND User = 'cam_usr';
GRANT ALL PRIVILEGES ON empresa.* TO 'root'@'%';
FLUSH PRIVILEGES;

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
  
  INSERT INTO Funcionario (nome, cpf, rg, sexo, data_nascimento, habilitacao, salario, carga_horaria)
  VALUES (@nome, @cpf, @rg, @sexo, @data_nascimento, @habilitacao, @salario, @carga_horaria);
END$$

CREATE PROCEDURE sp_select_all_funcionario()
BEGIN
  SELECT * FROM Funcionario;
END$$

CREATE PROCEDURE sp_select_funcionario_by_id(IN func_id INT)
BEGIN
  SELECT * FROM Funcionario WHERE id = func_id;
END$$

CREATE PROCEDURE sp_update_funcionario(IN func_id INT, IN func_data JSON)
BEGIN
  UPDATE Funcionario SET
    nome = JSON_EXTRACT(func_data, "$.nome"),
    cpf = JSON_EXTRACT(func_data, "$.cpf"),
    rg = JSON_EXTRACT(func_data, "$.rg"),
    sexo = JSON_EXTRACT(func_data, "$.sexo"),
    data_nascimento = JSON_EXTRACT(func_data, "$.data_nascimento"),
    habilitacao = JSON_EXTRACT(func_data, "$.habilitacao"),
    salario = JSON_EXTRACT(func_data, "$.salario"),
    carga_horaria_semanal = JSON_EXTRACT(func_data, "$.carga_horaria_semanal"),
    departamento_id = JSON_EXTRACT(func_data, "$.departamento_id")
  WHERE id = func_id;
END$$

CREATE PROCEDURE sp_delete_funcionario_by_id(IN func_id INT)
BEGIN
  DELETE FROM Funcionario WHERE id = func_id;
END$$

-- departamento
CREATE PROCEDURE sp_insert_departamento(IN json_str JSON)
BEGIN
  SET @nome = JSON_EXTRACT(json_str, '$.nome');

  INSERT INTO Departamento (nome)
  VALUES (@nome);
END$$

CREATE PROCEDURE sp_select_departamento(IN dep_id INT)
BEGIN
  SELECT * FROM Departamento WHERE id = dep_id;
END$$

CREATE PROCEDURE sp_update_departamento(IN dep_id INT, IN json_str JSON)
BEGIN
  SET @nome = JSON_EXTRACT(json_str, '$.nome');

  UPDATE Departamento SET
    nome = @nome
  WHERE id = dep_id;
END$$

CREATE PROCEDURE sp_delete_departamento(IN dep_id INT)
BEGIN
  DELETE FROM Departamento WHERE id = dep_id;
END$$

-- projeto
CREATE PROCEDURE sp_insert_projeto(IN json_data JSON)
BEGIN
  SET @nome = JSON_EXTRACT(json_data, '$.nome');
  SET @horas_necessarias = JSON_EXTRACT(json_data, '$.horas_necessarias');
  SET @prazo_estimado = JSON_EXTRACT(json_data, '$.prazo_estimado');
  SET @supervisor_id = JSON_EXTRACT(json_data, '$.supervisor_id');
  SET @departamento_id = JSON_EXTRACT(json_data, '$.departamento_id');

  INSERT INTO Projeto (nome, horas_necessarias, prazo_estimado, supervisor_id, departamento_id)
  VALUES (@nome, @horas_necessarias, @prazo_estimado, @supervisor_id, @departamento_id);
END$$

CREATE PROCEDURE sp_select_projeto_by_id(IN proj_id INT)
BEGIN
  SELECT * FROM Projeto WHERE id = proj_id;
END$$

CREATE PROCEDURE sp_update_projeto(IN proj_id INT, IN json_data JSON)
BEGIN
  UPDATE Projeto SET
    nome = JSON_EXTRACT(json_data, '$.nome'),
    horas_necessarias = JSON_EXTRACT(json_data, '$.horas_necessarias'),
    prazo_estimado = JSON_EXTRACT(json_data, '$.prazo_estimado'),
    supervisor_id = JSON_EXTRACT(json_data, '$.supervisor_id'),
    departamento_id = JSON_EXTRACT(json_data, '$.departamento_id')
  WHERE id = proj_id;
END$$

CREATE PROCEDURE sp_delete_projeto(IN proj_id INT)
BEGIN
  DELETE FROM Projeto WHERE id = proj_id;
END$$

-- projeto_funcionario
CREATE PROCEDURE sp_insert_projeto_funcionario(
    IN projeto_id INT,
    IN funcionario_id INT,
    IN carga_horaria_semanal DECIMAL(4,2)
)
BEGIN
    INSERT INTO Projeto_Funcionario (projeto_id, funcionario_id, carga_horaria_semanal)
    VALUES (projeto_id, funcionario_id, carga_horaria_semanal);
END$$

CREATE PROCEDURE sp_update_projeto_funcionario(
    IN projeto_id INT,
    IN funcionario_id INT,
    IN carga_horaria_semanal DECIMAL(4,2)
)
BEGIN
    UPDATE Projeto_Funcionario
    SET carga_horaria_semanal = carga_horaria_semanal
    WHERE projeto_id = projeto_id AND funcionario_id = funcionario_id;
END$$

CREATE PROCEDURE sp_delete_projeto_funcionario(
    IN projeto_id INT,
    IN funcionario_id INT
)
BEGIN
    DELETE FROM Projeto_Funcionario
    WHERE projeto_id = projeto_id AND funcionario_id = funcionario_id;
END$$

CREATE PROCEDURE sp_select_projeto_funcionario(IN projeto_id INT)
BEGIN
    SELECT pf.projeto_id, pf.funcionario_id, pf.carga_horaria_semanal,
    p.nome as nome_projeto, f.nome as nome_funcionario
    FROM Projeto_Funcionario pf
    JOIN Projeto p ON pf.projeto_id = p.id
    JOIN Funcionario f ON pf.funcionario_id = f.id
    WHERE pf.projeto_id = projeto_id;
END$$

-- FIM da Criação das Storage Procedures

DELIMITER ;

