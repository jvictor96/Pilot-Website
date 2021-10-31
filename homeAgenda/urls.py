from django.urls import path, include
from . import views, email

urlpatterns = [
    path('', views.index, name='Aindex'),
    path('/novaTarefa', views.novaTarefa, name='Anew'),
    path('/historico/<int:history>', views.index, name='Ahistorico'),

    path('/buscaEtiqueta/<str:etq>', views.index, name='AbuscaEtiqueta'),
    path('/buscaData/<int:data>', views.buscaData, name='AbuscaData'),

    path('/detalheTarefa/<str:tarefa>', views.buscaData, name='Atarefa'),
    path('/acao/<str:label>/<str:tarefa>', views.acao, name='Aacao'),
]