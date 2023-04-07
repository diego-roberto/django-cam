from rest_framework import serializers
from .models import Departamento, Funcionario, Projeto, Projeto_Funcionario


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'


class FuncionarioSerializer(serializers.ModelSerializer):
    departamento_nome = serializers.CharField(source='departamento.nome', read_only=True)

    class Meta:
        model = Funcionario
        fields = '__all__'


class ProjetoSerializer(serializers.ModelSerializer):
    supervisor_nome = serializers.CharField(source='supervisor.nome', read_only=True)
    departamento_nome = serializers.CharField(source='departamento.nome', read_only=True)

    class Meta:
        model = Projeto
        fields = '__all__'


class ProjetoFuncionarioSerializer(serializers.ModelSerializer):
    projeto_nome = serializers.CharField(source='projeto.nome', read_only=True)
    funcionario_nome = serializers.CharField(source='funcionario.nome', read_only=True)

    class Meta:
        model = Projeto_Funcionario
        fields = '__all__'
