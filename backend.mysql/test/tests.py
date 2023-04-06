import unittest
import mysql.connector

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="cam_usr",
            password="secret",
            database="empresa"
        )
        self.cursor = self.db.cursor()

    def test_connection(self):
        self.assertTrue(self.db.is_connected())

    def test_department_crud(self):
        # teste de criação de departmento
        query = "INSERT INTO Departamento (nome) VALUES (%s)"
        values = ("Departmento de Teste",)
        self.cursor.execute(query, values)
        self.db.commit()
        self.assertEqual(self.cursor.rowcount, 1)

        # teste de seleção de departmento
        query = "SELECT nome FROM Departamento WHERE id = %s"
        values = (1,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        self.assertEqual(result[0], "Departmento de Teste")

        # teste de update de departmento
        query = "UPDATE Departamento SET nome = %s WHERE id = %s"
        values = ("Departmento de Teste - o Retorno do Teste", 1)
        self.cursor.execute(query, values)
        self.db.commit()
        self.assertEqual(self.cursor.rowcount, 1)

        # teste de exclusão de departmento
        query = "DELETE FROM Departamento WHERE id = %s"
        values = (1,)
        self.cursor.execute(query, values)
        self.db.commit()
        self.assertEqual(self.cursor.rowcount, 1)

    def tearDown(self):
        self.cursor.close()
        self.db.close()

if __name__ == '__main__':
    unittest.main()
    
