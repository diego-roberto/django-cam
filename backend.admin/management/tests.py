from django.test import TestCase
from .models import Departamento, Funcionario, Projeto

class DepartamentoTest(TestCase):
    def setUp(self):
        self.departamento = Departamento.objects.create(nome='Departamento 1')

    def test_departamento_str(self):
        self.assertEqual(str(self.departamento), 'Departamento 1')

    def test_departamento_nome_unique(self):
        departamento2 = Departamento(nome='Departamento 1')
        with self.assertRaises(Exception):
            departamento2.save()

    def test_departamento_sem_nome(self):
        with self.assertRaises(Exception):
            departamento = Departamento()
            departamento.full_clean()

class FuncionarioTest(TestCase):
    def setUp(self):
        self.departamento = Departamento.objects.create(nome='Departamento 1')
        self.funcionario = Funcionario.objects.create(
            nome='Funcionario 1',
            cpf='12345678901',
            rg='12345678',
            sexo='M',
            data_nascimento='2000-01-01',
            habilitacao=True,
            salario=2000,
            carga_horaria_semanal=40,
            departamento=self.departamento,
        )

    def test_funcionario_str(self):
        self.assertEqual(str(self.funcionario), 'Funcionario 1')

    def test_funcionario_cpf_unique(self):
        funcionario2 = Funcionario(
            nome='Funcionario 2',
            cpf='12345678901',
            rg='12345679',
            sexo='F',
            data_nascimento='2001-01-01',
            habilitacao=True,
            salario=3000,
            carga_horaria_semanal=30,
            departamento=self.departamento,
        )
        with self.assertRaises(Exception):
            funcionario2.save()

    def test_funcionario_sem_nome(self):
        with self.assertRaises(Exception):
            funcionario = Funcionario()
            funcionario.full_clean()

class ProjetoTest(TestCase):
    def setUp(self):
        self.departamento = Departamento.objects.create(nome='Departamento 1')
        self.supervisor = Funcionario.objects.create(
            nome='Supervisor',
            cpf='12345678901',
            rg='12345678',
            sexo='M',
            data_nascimento='2000-01-01',
            habilitacao=True,
            salario=3000,
            carga_horaria_semanal=40,
            is_supervisor=True,
            departamento=self.departamento,
        )
        self.projeto = Projeto.objects.create(
            nome='Projeto 1',
            horas_necessarias=100,
            prazo_estimado='2023-05-31',
            supervisor=self.supervisor,
            departamento=self.departamento,
        )

    def test_projeto_str(self):
        self.assertEqual(str(self.projeto), 'Projeto 1')

    def test_projeto_nome_unique(self):
        projeto2 = Projeto(
            nome='Projeto 1',
            horas_necessarias=200,
            prazo_estimado='2023-06-30',
            supervisor=self.supervisor,
            departamento=self.departamento,
        )
        with self.assertRaises(Exception):
            projeto2.save()

    def test_projeto_hora_realizadas_menor_que_total(self):
        self.projeto.horas_realizadas = 200
        self.projeto.carga_horaria_total = 100
        with self.assertRaises(Exception):
            self.projeto.save()
