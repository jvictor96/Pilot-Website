import random
from django.shortcuts import render, redirect
from .models import Coisa, Grupo, GrupoCell
from homeAgenda.models import Perfis
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from datetime import datetime
from . import myscript

def index(request, **kwargs):
    user = auth.get_user(request)
    if not user.is_authenticated:
        return render(request, 'home/index.html', {'grupos':[]})

    Gids = myscript.grupos(request, nosQuaisFuiAceito=True)
    Gids = set(Gids)
    lista = []

    for id in Gids:
        lista.append(Grupo.objects.get(id=id))
        lista[-1].coisas = Coisa.objects.filter(grupo=id)[:10]
        lista[-1].etiquetas = []
        lista[-1].titulos = []
        coisas = Coisa.objects.filter(grupo=id)
        for coisa in coisas:
            lista[-1].etiquetas.append(coisa.tag)
            lista[-1].titulos.append(coisa.titulo)
        lista[-1].etiquetas = set(lista[-1].etiquetas)
        lista[-1].titulos = set(lista[-1].titulos)

    for grupo in Grupo.objects.filter(dono=user.email):
        lista.append(Grupo.objects.get(id=grupo.id))
        lista[-1].coisas = Coisa.objects.filter(grupo=grupo.id)[:10]
        lista[-1].etiquetas = []
        lista[-1].titulos = []
        coisas = Coisa.objects.filter(grupo=grupo.id)
        for coisa in coisas:
            lista[-1].etiquetas.append(coisa.tag)
            lista[-1].titulos.append(coisa.titulo)
        lista[-1].etiquetas = set(lista[-1].etiquetas)
        lista[-1].titulos = set(lista[-1].titulos)

    return render(request, 'home/index.html', {'grupos':lista, 'key':'index'})


@login_required(redirect_field_name='index')
def new(request):
    user = auth.get_user(request)
    if request.method != 'POST':
        Gids = myscript.grupos(request)
        listaG = []
        listaE = []
        listaT = []
        for grupo in Grupo.objects.filter(dono=user.email):
            listaG.append(grupo.titulo)
            coisas = Coisa.objects.filter(grupo=grupo.titulo)
            for coisa in coisas:
                listaE.append(coisa.tag)
                listaT.append(coisa.titulo)

        for id in Gids:
            grupo = Grupo.objects.get(id=id)
            listaG.append(grupo.titulo)
            coisas = Coisa.objects.filter(grupo=grupo.id)
            for coisa in coisas:
                listaE.append(coisa.tag)
                listaT.append(coisa.titulo)

        return render(request, 'home/new.html', {'agora':datetime.now().strftime('%Y-%m-%dT%H:%M'), 'grupos':listaG,
                                                 'titulos':listaT, 'tags':listaE})

    titulo = request.POST.get('titulo')
    dono = request.POST.get('dono')
    contagem = request.POST.get('contagem')
    email = request.POST.get('email')
    tag = request.POST.get('tag')

    grp = ''
    grupos = []
    Gids = myscript.grupos(request)
    for id in Gids:
        grupos.append(Grupo.objects.get(id=id))
    for grupo in Grupo.objects.filter(dono=user.email):
        grupos.append(grupo)
    for grupo in grupos:
        if grupo.titulo == request.POST.get('grupo'):
            grp = grupo.id


    coisa = Coisa(titulo=titulo, dono=dono, cont=contagem, email=email,
                    grupo=grp)
    if tag:
        coisa = Coisa(titulo=titulo, dono=dono, cont=contagem, email=email,
                  tag=tag, grupo=grp)

    coisa.save()
    return redirect('index')


@login_required(redirect_field_name='index')
def novoGrupo(request):
    if request.method != 'POST':
        return render(request,'home/novoGrupo.html')

    user=auth.get_user(request)
    titulo = request.POST.get('titulo')
    dono = request.POST.get('dono')
    tag = request.POST.get('tag')

    if request.POST.get('edita'):
        editaGrupo(request, request.POST.get('id'))
        return redirect('grupos/'+user.email)

    if Grupo.objects.filter(dono=dono, titulo=titulo):
        messages.add_message(request, messages.WARNING, "Você ja possui em grupo com esse nome")
        return redirect('grupos/'+user.email)

    if request.POST.get('pub'):
        pub = True
    else:
        pub = False

    if request.POST.get('open'):
        open = True
    else:
        open = False
    grupo = Grupo(titulo=titulo, dono=dono, pub=pub, open=open, tag=tag)
    grupo.save()

    messages.add_message(request, messages.SUCCESS, "Grupo criado com sucesso")
    return redirect('grupos/'+user.email)


@login_required(redirect_field_name='index')
def editaGrupo(request, id):
    user = auth.get_user(request)
    if user.email == Grupo.objects.get(id=id).dono:
        if request.method == "POST":
            titulo = request.POST.get('titulo')
            tag = request.POST.get('tag')
            if request.POST.get('pub'):
                pub = True
            else:
                pub = False
            if request.POST.get('open'):
                open = True
            else:
                open = False
            Grupo.objects.filter(id=id).update(titulo=titulo, tag=tag, pub=pub, open=open)
        else:
            grupo = Grupo.objects.get(id=id)
            pub, open = '', ''
            if grupo.pub:
                pub = 'checked'
            if grupo.open:
                open = 'checked'
            return render(request, 'home/novoGrupo.html', {'grupo': grupo, 'pub': pub, 'open': open, 'editando': 'checked'})
    else:
        messages.add_message(request, messages.WARNING, "Você não é dono do grupo que está tentando acessar")


@login_required(redirect_field_name='index')
def sair(request, id):
    user = auth.get_user(request)
    GrupoCell.objects.get(parent=id, email=user.email).delete()
    return fGrupos(request, user.email)


@login_required(redirect_field_name='index')
def fGrupos(request, nome):
    user=auth.get_user(request)
    if user.email!=nome:
        return index(request)

    meusGrupos = Grupo.objects.filter(dono=nome)
    for grupo in meusGrupos:
        if GrupoCell.objects.filter(aproved=False, parent=grupo.id).exists():
            grupo.alerta=True
        else:
            grupo.alerta=False


    gruposAlheios = GrupoCell.objects.filter(email=nome)
    grupos = []

    for grupoCell in gruposAlheios:
        grupos.append(Grupo.objects.get(id=grupoCell.parent))
        grupos[-1].aproved = grupoCell.aproved

    grupos = set(grupos)
    for grupo in grupos:
        grupo.membros=GrupoCell.objects.filter(parent=grupo.id, aproved=True).__len__()

    for grupo in meusGrupos:
        grupo.membros=GrupoCell.objects.filter(parent=grupo.id, aproved=True).__len__()

    return render(request, 'home/grupos.html', {'grupos': grupos, 'meusGrupos': meusGrupos})


@login_required(redirect_field_name='index')
def fGrupo(request, id):
    user = auth.get_user(request)
    grupo = Grupo.objects.get(id=id)
    membros=GrupoCell.objects.filter(parent=grupo.id)

    if user.email == grupo.dono:
        return render(request, 'home/grupo.html', {'grupo': grupo, 'membros':membros, 'dono':True})

    emails = []
    for membro in membros:
        emails.append(membro.email)
    if user.email in emails:
        return render(request, 'home/grupo.html', {'grupo': grupo, 'membros':membros})

    return fGrupos(request, user.email)


@login_required(redirect_field_name='index')
def convite(request, id):
    user = auth.get_user(request)
    grupo = Grupo.objects.get(id=id)

    if not GrupoCell.objects.filter(email=user.email, parent=grupo.id).exists()\
            and not Grupo.objects.filter(titulo=grupo.titulo, dono=user.email).exists():
        pedido = GrupoCell(email=user.email, parent=grupo.id)
        if grupo.open:
            pedido = GrupoCell(email=user.email, parent=grupo.id, aproved=True)
        pedido.save()
        messages.add_message(request, messages.WARNING, "A sua solicitação foi enviada com sucesso")
    else:
        messages.add_message(request, messages.WARNING, "A sua solicitação já foi enviada antes, se ela ainda não foi"
                                                        " aceita, entre em contato com o gerente do grupo")

    return fGrupos(request, user.email)


@login_required(redirect_field_name='index')
def acaoMembro(request, grupo, membro, acao):
    user = auth.get_user(request)
    if user.email == Grupo.objects.get(id = grupo).dono:
        if acao == "expulsar":
            GrupoCell.objects.filter(parent = grupo, email = membro).delete()
        if acao == "aprovar":
            GrupoCell.objects.filter(parent = grupo, email = membro).update(aproved=True)

    return fGrupo(request, grupo)


def buscaTitulo(request, grupo, tit):
    user = auth.get_user(request)
    coisas = Coisa.objects.filter(titulo=tit, grupo=grupo).order_by('-data')
    grupo = Grupo.objects.get(id=grupo)
    paginator = Paginator(coisas, 12)

    membros=GrupoCell.objects.filter(parent=grupo.id)
    ok = False
    for membro in membros:
        if user.email == membro.email:
            ok = True

    if ok or user.email == grupo.dono or grupo.pub:
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/index.html', {'coisas':page_obj, 'key':'titulo', 'grp':grupo})

    return index(request)


def buscaDono(request, grupo, don):
    user = auth.get_user(request)
    coisas = Coisa.objects.filter(dono=don, grupo=grupo).order_by('-data')
    grupo = Grupo.objects.get(id=grupo)
    paginator = Paginator(coisas, 12)

    membros=GrupoCell.objects.filter(parent=grupo.id)
    ok = False
    for membro in membros:
        if user.email == membro.email:
            ok = True

    if ok or user.email == grupo.dono or grupo.pub:
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/index.html', {'coisas':page_obj, 'key':'dono', 'grp':grupo})

    return index(request)


def buscaTag(request, grupo, tag):
    user = auth.get_user(request)
    coisas = Coisa.objects.filter(tag=tag, grupo=grupo).order_by('-data')
    grupo = Grupo.objects.get(id=grupo)
    paginator = Paginator(coisas, 12)

    membros=GrupoCell.objects.filter(parent=grupo.id)
    ok = False
    for membro in membros:
        if user.email == membro.email:
            ok = True

    if ok or user.email == grupo.dono or grupo.pub:
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/index.html', {'coisas':page_obj, 'key':'tag', 'grp':grupo})

    return index(request)


def buscaGrupo(request, grupo):
    user = auth.get_user(request)
    coisas = Coisa.objects.filter(grupo=grupo).order_by('-data')
    grupo = Grupo.objects.get(id=grupo)
    paginator = Paginator(coisas, 12)

    membros=GrupoCell.objects.filter(parent=grupo.id)
    ok = False
    for membro in membros:
        if user.email == membro.email:
            ok = True

    if ok or user.email == grupo.dono or grupo.pub:
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/index.html', {'coisas':page_obj, 'key':'grupo', 'grp':grupo})

    return index(request)
