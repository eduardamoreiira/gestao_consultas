# Generated by Django 5.1.4 on 2025-02-25 22:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('paciente', '__first__'),
        ('profissional', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id_consulta', models.AutoField(primary_key=True, serialize=False)),
                ('dt_consulta', models.DateTimeField(auto_now_add=True)),
                ('hr_consulta', models.TimeField(auto_now_add=True)),
                ('id_paciente', models.ForeignKey(db_column='id_paciente', on_delete=django.db.models.deletion.DO_NOTHING, to='paciente.paciente')),
                ('id_profissional', models.ForeignKey(db_column='id_profissional', on_delete=django.db.models.deletion.DO_NOTHING, to='profissional.profissional')),
            ],
            options={
                'db_table': 'consulta',
            },
        ),
    ]
