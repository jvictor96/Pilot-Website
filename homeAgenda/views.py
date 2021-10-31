from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Tarefas, Progressos, Perfis
from datetime import datetime, timedelta
from django.contrib import messages


def index(request, etq="nulo", history=0, alerta=''):
    user = auth.get_user(request)
    if history == 1:
        alerta = "Você está vendo registros antigos"
    elif alerta == '':
        alerta = "Sem tarefas importantes por perto"

    if etq == 'nulo':
        pontuais = Tarefas.objects.filter(prazo=None, dono=user.username)
        agendadas = Tarefas.objects.filter(ag=True, dono=user.username).order_by('prazo')
    else:
        pontuais = Tarefas.objects.filter(prazo=None, dono=user.username, tag=etq)
        agendadas = Tarefas.objects.filter(ag=True, dono=user.username, tag=etq).order_by('prazo')

    futurasPontuais = []
    for t in pontuais:
        if not t.feita and history == 0:
            futurasPontuais.append(t)
        if t.feita and history > 0:
            futurasPontuais.append(t)

    futuras = []
    for t in agendadas:
        timedelta = datetime(t.prazo.year, t.prazo.month, t.prazo.day) - \
                    datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        if (timedelta.days >= 0 and not t.feita) and history == 0:
            futuras.append(t)
        if (timedelta.days < 0 or t.feita) and history != 0:
            futuras.append(t)

    a = False
    for t in futuras:
        timedelta = datetime(t.prazo.year,t.prazo.month,t.prazo.day) - \
                    datetime(datetime.now().year,datetime.now().month, datetime.now().day)
        if timedelta.days == 0:
            alerta = "Há uma tarefa importante para hoje!"
            a=True

    for t in futuras:
        timedelta = datetime(t.prazo.year,t.prazo.month,t.prazo.day) - \
                    datetime(datetime.now().year,datetime.now().month, datetime.now().day)
        if timedelta.days==1:
            if a:
                alerta += ' Há também um outra para amanhã!!!'
            else:
                alerta = "Há uma tarefa para amanhã!"

    return render(request, 'homeAgenda/index.html', {'agendadas':futuras,'pontuais':futurasPontuais, 'alerta':alerta,
                                                     'history':history, 'etq':etq})

def buscaData(request, data):
    user = auth.get_user(request)
    pontuais = Tarefas.objects.filter(prazo=None, dono=user.username)
    agendadas = Tarefas.objects.filter(ag=True, dono=user.username)

    futuras = []
    for t in agendadas:
        timedelta = datetime(t.prazo.year,t.prazo.month,t.prazo.day) - \
                    datetime(datetime.now().year,datetime.now().month, datetime.now().day)
        if timedelta.days>=0:
            futuras.append(t)

    setList = []
    if data == 0:
        alerta = "Buscando tarefas para hoje"
        for t in agendadas:
            timedelta = t.prazo.day - datetime.now().day
            if timedelta == 0:
                setList.append(t)
        return render(request, 'homeAgenda/index.html', {'agendadas':setList,'pontuais':pontuais, 'alerta':alerta})

    if abs(data) == 1:
        alerta = "Buscando tarefas para amanhã"
        for t in futuras:
            timedelta = t.prazo.day - datetime.now().day
            if timedelta == data:
                setList.append(t)
        return render(request, 'homeAgenda/index.html', {'agendadas':setList,'pontuais':pontuais, 'alerta':alerta})

    if abs(data) == 2:                      #ainda essa semana
        alerta = "Buscando tarefas para essa semana"
        for t in futuras:
            timedelta = datetime(t.prazo.year,t.prazo.month,t.prazo.day) - \
                        datetime(datetime.now().year,datetime.now().month, datetime.now().day)
            if timedelta.days<7*data/2:
                setList.append(t)
        return render(request, 'homeAgenda/index.html', {'agendadas':setList,'pontuais':pontuais, 'alerta':alerta})

    if abs(data) == 3:                      #semana que vem
        alerta = "Buscando tarefas para semana que vem"
        for t in futuras:
            timedelta = datetime(t.prazo.year,t.prazo.month,t.prazo.day) - \
                        datetime(datetime.now().year,datetime.now().month, datetime.now().day)
            if timedelta.days>7*data/3 and timedelta.days<14*data/3:
                setList.append(t)
        return render(request, 'homeAgenda/index.html', {'agendadas': setList, 'pontuais': pontuais, 'alerta': alerta})

    if abs(data) == 4:                      #ainda esse mes
        alerta = "Buscando tarefas desse mês"
        for t in futuras:
            timedelta = t.prazo.month - datetime.now().month
            if timedelta == 0:
                setList.append(t)
        return render(request, 'homeAgenda/index.html', {'agendadas': setList, 'pontuais': pontuais, 'alerta': alerta})

    if abs(data) == 5:                      #mes que vem
        alerta = "Buscando tarefas do mês que vem"
        for t in futuras:
            timedelta = t.prazo.month - datetime.now().month
            if timedelta == 1:
                setList.append(t)
        return render(request, 'homeAgenda/index.html', {'agendadas': setList, 'pontuais': pontuais, 'alerta': alerta})


def tarefa(request, id):
    t = Tarefas.objects.get(id=id)
    return render(request, 'homeAgenda/tarefa.html', {'tarefa': t})


@login_required(redirect_field_name='index')
def novaTarefa(request):
    user = auth.get_user(request)
    if request.method != 'POST':
        tarefas = Tarefas.objects.filter(dono=user.username)
        listaT = []
        for tarefa in tarefas:
            listaT.append(tarefa.tag)
        listaT = set(listaT)
        return render(request, 'homeAgenda/new.html', {'tags':listaT})

    nome = request.POST.get('nome')
    desc = request.POST.get('desc')
    dono = request.POST.get('dono')
    tag = request.POST.get('tag')
    prazo = request.POST.get('prazo')

    if not nome or not tag:
        messages.add_message(request, messages.WARNING, 'Os campos "Título" e "Etiqueta" não podem ficar vazios')
        return render(request, 'homeAgenda/new.html', {'dono':dono, 'nome':nome, 'desc':desc, 'tag':tag, 'prazo':prazo})

    if request.POST.get('edita'):
        editaTarefa(request, request.POST.get('id'))
        return index(request)

    coisa = Tarefas(nome=nome, dono=dono, tag=tag)
    if desc:
        coisa = Tarefas(nome=nome, dono=dono, tag=tag, desc=desc)
    if prazo:
        coisa = Tarefas(nome=nome, dono=dono, tag=tag, prazo=prazo, ag=True)
    if desc and prazo:
        coisa = Tarefas(nome=nome, dono=dono, tag=tag, desc=desc, prazo=prazo, ag=True)
    coisa.save()

    return index(request)

def editaTarefa(request, id):
    nome = request.POST.get('nome')
    desc = request.POST.get('desc')
    dono = request.POST.get('dono')
    tag = request.POST.get('tag')
    prazo = request.POST.get('prazo')

    if desc and prazo:
        Tarefas.objects.filter(id=id).update(nome=nome, desc=desc, dono=dono, tag=tag, prazo=prazo, ag=True)
    elif desc:
        Tarefas.objects.filter(id=id).update(nome=nome, desc=desc, dono=dono, tag=tag, ag=False)
    elif prazo:
        Tarefas.objects.filter(id=id).update(nome=nome, dono=dono, tag=tag, prazo=prazo, ag=True)
    else:
        Tarefas.objects.filter(id=id).update(nome=nome, dono=dono, tag=tag, ag=False)


def login(request):
    senha = request.POST.get('senha')
    usuario = request.POST.get('usuario')
    if User.objects.filter(username=usuario).exists():
        user = auth.authenticate(request, username=usuario, password=senha)
        if user:
            auth.login(request,user)
        else:
            pass

    return redirect('index')


def acao(request, label, tarefa):
    user = auth.get_user(request)

    if not Tarefas.objects.get(id=tarefa).dono == user.username:
        return index(request, alerta='A tarefa com o id apontado não pertence ao email logado')

    if label == 'Apagar':
        Tarefas.objects.filter(id=tarefa).delete()
        return index(request, alerta='A tarefa foi deletada, olha lá o que está fazendo, heim')

    if label == 'Comentar':
        return index(request, alerta='Ainda estou trabalhando na função de comentar')

    if label == 'Editar':
        if Tarefas.objects.get(id=tarefa).ag:
            return render(request, "homeAgenda/new.html", {'tarefa':Tarefas.objects.get(id=tarefa),
                                                       'agora':Tarefas.objects.get(id=tarefa).prazo.strftime('%Y-%m-%dT%H:%M'),
                                                       'editando':'checked'})
        else:
            return render(request, "homeAgenda/new.html", {'tarefa':Tarefas.objects.get(id=tarefa), 'editando':'checked'})

    if label == 'Encerrar':
        Tarefas.objects.filter(id=tarefa).update(feita = True)
        return index(request, alerta='Uhull, parabéns!')

    if label == 'Favoritar':
        if(Tarefas.objects.get(id=tarefa).fav):
            Tarefas.objects.filter(id=tarefa).update(fav = False)
            return index(request)
        else:
            Tarefas.objects.filter(id=tarefa).update(fav = True)
            return index(request)


def logon(request):
    if request.method != 'POST':
        return render(request, 'homeAgenda/register.html')

    email = request.POST.get('email')
    senha = request.POST.get('senha')
    usuario = request.POST.get('usuario')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    chave = request.POST.get('chave')
    codigo = request.POST.get('codigo')
    savings = {'email':email, 'usuario':usuario, 'nome':nome, 'sobrenome':sobrenome}

    if chave != codigo:
        messages.add_message(request, messages.WARNING, 'A chave inserida não coincide com a enviada por e-mail')
        return render(request, 'homeAgenda/register.html', savings)

    if User.objects.filter(username=usuario, email=email).exists():
        return redirect('register')
    else:

        user=User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome,
                                      last_name=sobrenome)
        user.save()
        user = auth.authenticate(request, username=usuario, password=senha)
        auth.login(request,user)

    return redirect('index')


def logout(request):
    auth.logout(request)
    return redirect('index')