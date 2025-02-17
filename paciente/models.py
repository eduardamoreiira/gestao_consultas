from django.db import models
from django.utils.timezone import now

class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    dt_nasc= models.DateField(null=True, blank=True)
    dt_cadastro = models.DateTimeField(default=now) #preenche a data e hora atual
    ativo = models.CharField(default='sim') #o paciente já vem ativo por padrão
    
    class Meta:
        db_table = 'paciente' 

    def __str__(self):
        return self.nome




