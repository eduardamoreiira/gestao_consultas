from django.db import models
from paciente.models import Paciente
from profissional.models import Profissional

class Consulta(models.Model):
    id_consulta = models.AutoField(primary_key=True)
    dt_consulta = models.DateField(auto_now_add=True)
    hr_consulta = models.TimeField(auto_now_add=True)
    id_profissional = models.ForeignKey(
        'profissional.Profissional',
        models.DO_NOTHING,
        db_column='id_profissional',
        to_field='id_profissional'  #garante que a FK usa o campo correto
    )
    id_paciente = models.ForeignKey(
        'paciente.Paciente',
        models.DO_NOTHING,
        db_column='id_paciente'
    )

    class Meta:
        db_table = 'consulta'
