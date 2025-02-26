from django.db import models

class Tratamento(models.Model):
    id_tratamento = models.AutoField(primary_key=True)
    tipo_tratamento = models.CharField(max_length=200)

    class Meta:
        db_table = 'tratamento'
