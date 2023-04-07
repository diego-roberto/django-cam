import unittest
import mysql.connector

class TestDatabase(unittest.TestCase):
    
    def setUp(self):        
        self.db = mysql.connector.connect(
            host="localhost",
            user="cam_usr",
            password="secret",
            database="empresa",
            connection_timeout=10,
            connect_timeout=20
        )
        self.cursor = self.db.cursor()

    def test_connection(self):
        print("Conectando na base de dados...")
        self.assertTrue(self.db.is_connected())
        if  self.db.is_connected():
            print("Conectado na base de dados: PASS \n")
            print("Iniciando testes na base de dados...")        

    def test_department_crud(self):

        # teste de inserção de departmento
        query = "INSERT INTO Departamento (nome) VALUES (%s)"
        values = ("Departamento de Teste",)
        self.cursor.execute(query, values)
        self.db.commit()
        self.assertEqual(self.cursor.rowcount, 1)
        if self.cursor.rowcount == 1:
            print("Teste de inserção: PASS")

        query = "SELECT LAST_INSERT_ID()"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        department_id = result[0]

        # teste de seleção de departmento
        query = "SELECT nome FROM Departamento WHERE id = %s"
        values = (department_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        self.assertEqual(result[0], "Departamento de Teste")
        if result[0] == "Departamento de Teste":
            print("Teste de leitura: PASS")

        # teste de update de departmento
        query = "UPDATE Departamento SET nome = %s WHERE id = %s"
        values = ("Departamento de Teste - Sob Nova Direção", department_id)
        self.cursor.execute(query, values)
        self.db.commit()
        query = "SELECT nome FROM Departamento WHERE id = %s"
        values = (department_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        self.assertEqual(result[0], "Departamento de Teste - Sob Nova Direção")
        if result is not None and result[0] == "Departamento de Teste - Sob Nova Direção":
            print("Teste de atualização: PASS")
        else:
            print("Teste de atualização: FAIL")


        # teste de exclusão de departamento
        query = "DELETE FROM Departamento WHERE id = %s"
        values = (department_id,)
        self.cursor.execute(query, values)
        self.db.commit()
        num_rows_deleted = self.cursor.rowcount
        self.assertEqual(num_rows_deleted, 1)
        if num_rows_deleted == 1:
            print("Teste de exclusão: PASS")


    def tearDown(self):
        self.cursor.close()
        self.db.close()

if __name__ == '__main__':
    unittest.main()

