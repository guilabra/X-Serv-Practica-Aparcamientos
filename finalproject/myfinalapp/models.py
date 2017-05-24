from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Aparcamiento(models.Model):
    nombre = models.CharField(max_length=256)
    accesibilidad = models.CharField(max_length=16)
    url = models.CharField(max_length=256)
    direccion = models.CharField(max_length=256)
    barrio = models.CharField(max_length=256)
    distrito = models.CharField(max_length=256)
    coordenadas = models.CharField(max_length=256)
    contacto = models.CharField(max_length=256)
    descripcion = models.TextField()

class Aparcamiento_Seleccionado(models.Model):
    aparcamiento_id = models.ForeignKey(Aparcamiento)
    usuario = models.ForeignKey(User, default="")
    fecha = models.DateField(auto_now=True)

class Comentario(models.Model):
    aparcamiento_id = models.ForeignKey(Aparcamiento) #relacion muchos a uno
    comentario = models.TextField()

class CSS(models.Model):
    usuario = models.CharField(max_length=256)
    titulo = models.CharField(max_length=256)
