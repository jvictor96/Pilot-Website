import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from datetime import datetime
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User


def emailConfirmacao(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    usuario = request.POST.get('usuario')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    chave = random.randint(0, 999999)
    savings = {'email':email, 'usuario':usuario, 'nome':nome, 'sobrenome':sobrenome}

    if not nome or not sobrenome or not senha or not email or not usuario:
        messages.add_message(request, messages.WARNING, 'Nenhum campo pode ficar vazio')
        return render(request, 'homeAgenda/register.html', savings)

    if User.objects.filter(email=email):
        messages.add_message(request, messages.WARNING, 'Já existe um usuário com este e-mail')
        return render(request, 'homeAgenda/register.html', savings)

    if User.objects.filter(username=usuario):
        messages.add_message(request, messages.WARNING, 'Já existe um usuário com este nome de usuário')
        return render(request, 'homeAgenda/register.html', savings)

    with open('homeAgenda/email.html','r') as html:
        template = Template(html.read())
        d_atual = datetime.now().strftime('%d/%m/%Y')
        corpoMsg = template.substitute(data=d_atual, chave= chave)

    msg = MIMEMultipart()
    msg['from'] = 'José Victor'
    msg['to'] = email
    msg['subject'] = 'Verificação de e-mail'

    corpo = MIMEText(corpoMsg,'html')
    msg.attach(corpo)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('jvictor96@gmail.com', 'oszdufwrxwfeyswi')
        smtp.send_message(msg)

    return render(request, 'homeAgenda/confirmaEmail.html', {'usuario':usuario, 'nome':nome, 'sobrenome':sobrenome,
                                                       'senha':senha, 'chave':chave, 'email':email})


