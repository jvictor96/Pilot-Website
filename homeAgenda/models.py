from django.db import models


class Tarefas(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    nome = models.CharField(max_length=64)
    dono = models.CharField(max_length=64)
    prazo = models.DateTimeField(null=True)
    ag = models.BooleanField(null=True)
    importante = models.BooleanField(null=True)
    desc = models.CharField(max_length=256, blank=True)
    comentario = models.CharField(max_length=256, blank=True)
    tag = models.CharField(max_length=64)
    repetir = models.IntegerField(default=0)
    feita = models.BooleanField(default=False)
    fav = models.BooleanField(default=False)
    parent = models.IntegerField(default=-1, blank=True)


class Progressos(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    parent = models.IntegerField()
    nome = models.CharField(max_length=64)
    carga = models.IntegerField(blank=True)


class Perfis(models.Model):
    usuario = models.CharField(max_length=16)
    horas = models.IntegerField(default=8)

# Create your models here.
