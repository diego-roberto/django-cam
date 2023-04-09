from django.db import models

class Departamento(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ('nome',)

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    nome = models.CharField(max_length=255, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    rg = models.CharField(max_length=9, unique=True)
    sexo = models.CharField(max_length=1)
    data_nascimento = models.DateField()
    habilitacao = models.BooleanField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    carga_horaria_semanal = models.DecimalField(max_digits=4, decimal_places=2)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'funcionario'
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ('nome',)

    def __str__(self):
        return self.nome

class Projeto(models.Model):
    nome = models.CharField(max_length=255)
    horas_necessarias = models.IntegerField()
    prazo_estimado = models.DateField()
    horas_realizadas = models.IntegerField()
    ultimo_calculo_horas = models.DateField()
    supervisor = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'projeto'
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ('prazo_estimado',)

    def __str__(self):
        return self.nome

class Projeto_Funcionario(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    carga_horaria_semanal = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = 'projeto_funcionario'
        unique_together = ('projeto', 'funcionario')

    def __str__(self):
        return f"{self.projeto} - {self.funcionario}"
    
