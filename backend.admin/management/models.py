from django.db import models
from datetime import datetime, timezone
from django.core.exceptions import ValidationError
import math

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
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    rg = models.CharField(max_length=9, unique=True, verbose_name="RG")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
    habilitacao = models.BooleanField(verbose_name="Possui habilitação")
    salario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salário")
    carga_horaria_semanal = models.PositiveSmallIntegerField(verbose_name="Carga horária semanal")
    is_supervisor = models.BooleanField(verbose_name="Função Supervisor", default=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    projetos = models.ManyToManyField('Projeto', through='Projeto_Funcionario', related_name='funcionarios_projetos')

    class Meta:
        db_table = 'funcionario'
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ('nome',)

    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            old = Funcionario.objects.get(pk=self.pk)
            if old.carga_horaria_semanal != self.carga_horaria_semanal:
                supervisao_projetos = Projeto.objects.filter(supervisor=self)
                total_carga_horaria = sum(projeto.horas_realizadas for projeto in supervisao_projetos)
                for projeto in supervisao_projetos:
                    total_carga_horaria += sum(
                        projeto_funcionario.carga_horaria_semanal
                        for projeto_funcionario in projeto.projeto_funcionario_set.all()
                        if projeto_funcionario.funcionario != self
                    )
                if total_carga_horaria > self.carga_horaria_semanal:
                    raise ValidationError(
                        f"Supervisor com carga horária excedida para o projeto {projeto.nome}."
                    )
        super().save(*args, **kwargs)

class Projeto(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    horas_necessarias = models.PositiveIntegerField()
    prazo_estimado = models.DateField()
    horas_realizadas = models.PositiveIntegerField(default=0)
    carga_horaria_total = models.PositiveIntegerField(default=0)
    ultimo_calculo_horas = models.DateField(null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='projetos')
    supervisor = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name='projetos_supervisionados',
    )
    funcionarios = models.ManyToManyField(
        Funcionario,
        through='Projeto_Funcionario',
        related_name='funcionarios_projetos',
        through_fields=('projeto', 'funcionario'),
        )

    class Meta:
        db_table = 'projeto'
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ('prazo_estimado',)

    def __str__(self):
        return self.nome

    def clean(self):
        if self.pk is None:
            return

        total_horas = self.horas_realizadas + sum(
            projeto_funcionario.funcionario.carga_horaria_semanal
            for projeto_funcionario in self.projeto_funcionario_set.all()
        )
        if total_horas > self.supervisor.carga_horaria_semanal:
            raise ValidationError(
                f"Supervisor com carga horária excedida para o projeto {self.nome}."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def remaining_hours(self):
        return self.horas_necessarias - self.horas_realizadas - sum(
            projeto_funcionario.funcionario.carga_horaria_semanal
            for projeto_funcionario in self.projeto_funcionario_set.all()
        )

    def update_horas_realizadas(self):
        if not self.ultimo_calculo_horas:
            self.ultimo_calculo_horas = timezone.now().date()
            self.save()

        semanas_desde_ultimo_calculo = (timezone.now().date() - self.ultimo_calculo_horas).days // 7
        total_carga_horaria = sum(
            projeto_funcionario.funcionario.carga_horaria_semanal
            for projeto_funcionario in self.projeto_funcionario_set.all()
        )
        self.horas_realizadas += total_carga_horaria * semanas_desde_ultimo_calculo
        self.ultimo_calculo_horas = timezone.now().date()
        self.save()

    def update_prazo_estimado(self):
        horas_restantes = self.horas_necessarias - self.horas_realizadas
        total_carga_horaria = sum(
            projeto_funcionario.funcionario.carga_horaria_semanal
            for projeto_funcionario in self.projeto_funcionario_set.all()
        )
        if not total_carga_horaria:
            self.prazo_estimado = None
        else:
            semanas_restantes = math.ceil(horas_restantes / total_carga_horaria)
            self.prazo_estimado = timezone.now().date() + datetime.timedelta(weeks=semanas_restantes)
        self.save()


    def add_funcionario(self, funcionario, carga_horaria_semanal, is_supervisor=False):
        projeto_funcionario = Projeto_Funcionario(
            projeto=self,
            funcionario=funcionario,
            carga_horaria_semanal=carga_horaria_semanal,
            is_supervisor=is_supervisor,
        )
        projeto_funcionario.full_clean()
        projeto_funcionario.save()
        self.refresh_from_db()

    def remove_funcionario(self, funcionario):
        self.funcionarios.remove(funcionario)
        self.refresh_from_db()

class Projeto_Funcionario(models.Model):
    FUNCAO_CHOICES = [
        ('F', 'Funcionário'),
        ('S', 'Supervisor'),
    ]
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    funcao = models.CharField(max_length=1, choices=FUNCAO_CHOICES, default='F')
    carga_horaria_semanal = models.PositiveSmallIntegerField(verbose_name="Carga horária semanal", default=0)

    class Meta:
        db_table = 'projeto_funcionario'
        unique_together = ('projeto', 'funcionario')

    def __str__(self):
        return f"{self.projeto} - {self.funcionario}"
    
    # def clean(self):
    #     total_horas = (
    #         self.carga_horaria_semanal
    #         + self.funcionario.projetofuncionario_set.exclude(id=self.id).aggregate(
    #             models.Sum('carga_horaria_semanal')
    #         )['carga_horaria_semanal__sum']
    #         + self.projeto.projeto_funcionario_set.exclude(id=self.id).aggregate(
    #             models.Sum('carga_horaria_semanal')
    #         )['carga_horaria_semanal__sum']
    #     )
    #     if total_horas > self.funcionario.carga_horaria_semanal:
    #         raise ValidationError(
    #             f"Funcionário {self.funcionario.nome} com carga horária excedida no projeto {self.projeto.nome}."
    #         )
    
    # def clean(self):
    #     for projeto_funcionario in self.projeto.funcionarios.all():
    #         if self.funcionario == projeto_funcionario.funcionario and self.pk != projeto_funcionario.pk:
    #             raise ValidationError("Funcionário já adicionado neste projeto")

    #     if self.carga_horaria_semanal <= 0:
    #         raise ValidationError('A carga horária deve ser maior que zero.')

    #     total_horas = self.carga_horaria_semanal + sum(
    #         pf.carga_horaria_semanal
    #         for pf in Projeto_Funcionario.objects.filter(funcionario=self.funcionario)
    #         if pf.pk != self.pk
    #     )

    #     if total_horas > self.funcionario.carga_horaria_semanal:
    #         raise ValidationError(f'A carga horária semanal excede a carga horária máxima do funcionário {self.funcionario.nome}.')

    #     total_horas_projeto = self.carga_horaria_semanal + sum(
    #         pf.carga_horaria_semanal
    #         for pf in self.projeto.projeto_funcionario_set.all()
    #         if pf.pk != self.pk
    #     )

    #     if total_horas_projeto > self.projeto.supervisor.carga_horaria_semanal:
    #         raise ValidationError(f'A carga horária semanal excede a carga horária máxima do supervisor {self.projeto.supervisor.nome} no projeto {self.projeto.nome}.')

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(*args, **kwargs)
    #     self.projeto.update_horas_realizadas()
    #     self.projeto.update_prazo_estimado()

    def clean(self):
        super().clean()

        if self.pk is None and self.projeto.projeto_funcionario_set.filter(funcionario=self.funcionario).exists():
            raise ValidationError('Funcionário já adicionado neste projeto')

        total_horas = self.carga_horaria_semanal + self.funcionario.projeto_funcionario.exclude(pk=self.pk).aggregate(models.Sum('carga_horaria_semanal'))['carga_horaria_semanal__sum']
        if total_horas > self.funcionario.carga_horaria_semanal:
            raise ValidationError(f'A carga horária semanal excede a carga horária máxima do funcionário {self.funcionario.nome}.')

        total_horas_projeto = self.carga_horaria_semanal + self.projeto.projeto_funcionario_set.exclude(pk=self.pk).aggregate(models.Sum('carga_horaria_semanal'))['carga_horaria_semanal__sum']
        if total_horas_projeto > self.projeto.supervisor.carga_horaria_semanal:
            raise ValidationError(f'A carga horária semanal excede a carga horária máxima do supervisor {self.projeto.supervisor.nome} no projeto {self.projeto.nome}.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.projeto.update_horas_realizadas()
        self.projeto.update_prazo_estimado()

