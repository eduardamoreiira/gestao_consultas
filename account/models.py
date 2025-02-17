from django.db import models


class Login(models.Model):
    id_login = models.AutoField(primary_key=True)
    tipo_acesso = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    senha = models.CharField(max_length=20)

    def __str__(self):
        return self.nome