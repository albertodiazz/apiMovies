from django.db import models

class Movies(models.Model):
    '''Aqui estan nuestra informacion de las peliculas'''
    Title = models.CharField(max_length=50)
    Genero = models.CharField(max_length=50)
    # Esta calificacion debe ser obtenida de IMBD
    Calification= models.IntegerField()
    # Hay que concantenar ya pueden ser varias urls
    URL = models.URLField(max_length=200)

class Keys(models.Model):
    '''Aqui almacenamos la informacion de nuestra Key de Gnula
    para hacer las peticiones'''
    Title = models.CharField(max_length=100)
    Key = models.CharField(max_length=300)
