# Generated by Django 5.1.4 on 2025-02-17 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id_login', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_acesso', models.CharField(max_length=20)),
                ('nome', models.CharField(max_length=100)),
                ('senha', models.CharField(max_length=20)),
            ],
        ),
    ]
