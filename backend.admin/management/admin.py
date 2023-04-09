from django.contrib import admin
from .models import Departamento, Funcionario, Projeto

class CustomAdminSite(admin.AdminSite):
    admin.site.site_header = 'CAM Admin'
    admin.site.site_title = 'CAM Admin'
    admin.site.index_title = 'Gerenciamento'

admin_site = CustomAdminSite()

admin.site.register(Departamento)
admin.site.register(Funcionario)
admin.site.register(Projeto)
