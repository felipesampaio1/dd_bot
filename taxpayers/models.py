from django.db import models
from django.utils import timezone


# Create your models here.
class Payers(models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255)
    payer_name = models.CharField(max_length=255)
    partner = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    initial_requirement = models.CharField(max_length=4000)
    inss_requirement = models.CharField(max_length=4000)
    doctor = models.BooleanField()
    social = models.BooleanField()
    der = models.DateField(null=True, blank=True)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f'Nome: {self.payer_name} - CPF: {self.cpf}'
