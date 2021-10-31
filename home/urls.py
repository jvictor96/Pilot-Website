"""piloto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views, email

urlpatterns = [
    path('', views.index, name='index'),
    path('buscaDono/<str:grupo>/<str:don>', views.buscaDono, name='buscaDono'),
    path('buscaTitulo/<str:grupo>/<str:tit>', views.buscaTitulo, name='buscaTitulo'),
    path('buscaTag/<str:grupo>/<str:tag>', views.buscaTag, name='buscaTag'),
    path('buscaGrupo/<int:grupo>', views.buscaGrupo, name='buscaGrupo'),

    path('log/Zlogin', views.Zlogin, name='Zlogin'),
    path('log/Zlogon/p1', views.register, name='logonPasso1'),
    path('log/Zlogon/p2', email.emailConfirmacao, name='logonPasso2'),
    path('log/Zlogon/p3', views.confirmaLogon, name='logonPasso3'),
    path('log/logout', views.logout, name='logout'),
    path('register', views.register, name='register'),

    path('new', views.new, name='new'),
    path('grupos/<str:nome>', views.fGrupos, name='grupos'),
    path('grupo/<int:id>', views.fGrupo, name='detalhaGrupo'),
    path('editaGrupo/<int:id>', views.editaGrupo, name='editaGrupo'),
    path('convite/<int:id>', views.convite),
    path('novoGrupo', views.novoGrupo, name='novoGrupo'),

    path('grupo/<str:grupo>/<str:membro>/<str:acao>', views.acaoMembro, name='acaoMembro'),
    path('grupo/sair/<int:id>', views.sair, name='sair'),
]
