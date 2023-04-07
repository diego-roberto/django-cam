from django.urls import path
from .views import DepartamentoList, DepartamentoDetail, FuncionarioList, FuncionarioDetail, ProjetoList, ProjetoDetail

urlpatterns = [
    path('departamentos/', DepartamentoList.as_view()),
    path('departamentos/<int:pk>/', DepartamentoDetail.as_view()),
    path('funcionarios/', FuncionarioList.as_view()),
    path('funcionarios/<int:pk>/', FuncionarioDetail.as_view()),
    path('projetos/', ProjetoList.as_view()),
    path('projetos/<int:pk>/', ProjetoDetail.as_view()),
]
