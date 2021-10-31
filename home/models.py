from django.db import models
import datetime


class Coisa(models.Model):
    titulo = models.CharField(max_length=64)
    dono = models.CharField(max_length=64)
    email = models.CharField(max_length=64, blank=True)
    tag = models.CharField(max_length=64, blank=True)
    grupo = models.CharField(max_length=64, blank=True)
    cont = models.CharField(max_length=8)
    data = models.DateTimeField(default=datetime.datetime.now())
    abs = models.BooleanField(default=False)


class Grupo(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    titulo = models.CharField(max_length=64)
    dono = models.CharField(max_length=64)
    pub = models.BooleanField(default=False)
    open = models.BooleanField(default=False)
    tag = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.titulo


class GrupoCell(models.Model):
    email = models.CharField(max_length=64)
    parent = models.IntegerField()
    aproved = models.BooleanField(default=False)

    def __str__(self):
        return self.email