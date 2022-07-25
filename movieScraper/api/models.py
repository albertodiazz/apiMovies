from django.db import models

# Create your models here.
class Movies(models.Model):

    Title = models.CharField(max_length=50)
    Genero = models.CharField(max_length=50)
    # Esta calificacion debe ser obtenida de IMBD
    Calification= models.IntegerField()
    # Hay que concantenar ya pueden ser varias urls
    URL = models.URLField(max_length=200)
