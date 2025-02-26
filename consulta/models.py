from django.db import models

class Consulta(models.Model):
    id_consulta = models.AutoField(primary_key=True)
    dt_consulta = models.DateTimeField(auto_now_add=True)
    hr_consulta = models.TimeField(auto_now_add=True)
    id_profissional = models.ForeignKey(
        'profissional.Profissional',
        models.DO_NOTHING,
        db_column='id_profissional',
        to_field='id_profissional'  # Garante que a FK usa o campo correto
    )
    id_paciente = models.ForeignKey(
        'paciente.Paciente',
        models.DO_NOTHING,
        db_column='id_paciente'
    )

    class Meta:
        db_table = 'consulta'
