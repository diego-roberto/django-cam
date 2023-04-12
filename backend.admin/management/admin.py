from django.contrib import admin
from .models import Departamento, Funcionario, Projeto
from .forms import FuncionarioForm, ProjetoAdminForm

class CustomAdminSite(admin.AdminSite):
    admin.site.site_header = 'CAM Admin'
    admin.site.site_title = 'CAM Admin'
    admin.site.index_title = 'Gerenciamento'

admin_site = CustomAdminSite()

class FuncionarioEntity(admin.ModelAdmin):
    form = FuncionarioForm

class DepartamentoAdmin(admin.ModelAdmin):
    def projetos(self, obj):
        return ([p.nome for p in obj.projetos.all()])
    
    list_display = ['nome', 'projetos']


class ProjetoAdmin(admin.ModelAdmin):
    form = ProjetoAdminForm
    

admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Funcionario, FuncionarioEntity)
admin.site.register(Projeto, ProjetoAdmin)

