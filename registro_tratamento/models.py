from django.db import models
from consulta.models import Consulta
from tratamento.models import Tratamento

class RegistroTratamento(models.Model):
    id_tratamento = models.AutoField(primary_key=True)
    dt_inicio = models.DateField()
    dt_fim = models.DateField()
    diagnostico = models.CharField(max_length=500)
    observacoes = models.CharField(max_length=1000)
    abordagem = models.CharField(max_length=300)
    id_consulta = models.ForeignKey(
        'consulta.Consulta',
        models.DO_NOTHING,
        db_column='id_consulta',
        to_field='id_consulta'
        )
    id_tratamento = models.ForeignKey(
        'tratamento.Tratamento',
        models.DO_NOTHING,
        db_column='id_tratamento',
        to_field='id_tratamento')

class Meta:
    db_table = 'registro_tratamento'