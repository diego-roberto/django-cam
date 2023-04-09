from django.urls import path
from .admin import admin_site
from .views import DepartamentoList, DepartamentoDetail, FuncionarioList, FuncionarioDetail, ProjetoList, ProjetoDetail

urlpatterns = [
    path('admin/', admin_site.urls),
    path('departamentos/', DepartamentoList.as_view()),
    path('departamentos/<int:pk>/', DepartamentoDetail.as_view()),
    path('funcionarios/', FuncionarioList.as_view()),
    path('funcionarios/<int:pk>/', FuncionarioDetail.as_view()),
    path('projetos/', ProjetoList.as_view()),
    path('projetos/<int:pk>/', ProjetoDetail.as_view()),
]
