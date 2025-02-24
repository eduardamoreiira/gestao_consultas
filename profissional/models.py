from django.db import models

class Profissional(models.Model):
    id_profissional = models.AutoField(primary_key=True)
    telefone = models.CharField(max_length=45)
    num_identificaco = models.CharField(max_length=45)
    sexo = models.CharField(max_length=1)
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class Meta:
    db_table = 'profissional'