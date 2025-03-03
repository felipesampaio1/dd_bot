import uuid

from django.db import models
from django.utils import timezone

# Create your models here.
class Payer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf = models.CharField(max_length=11, unique=True)
    passwd = models.CharField(blank=True, max_length=255)
    payer_name = models.CharField(blank=True, max_length=255)
    partner = models.CharField(blank=True, max_length=255)
    phone = models.CharField(blank=True, max_length=20)
    initial_requirement = models.CharField(blank=True, max_length=4000)
    inss_requirement = models.CharField(blank=True, max_length=4000)
    doctor = models.BooleanField(default=False)
    social = models.BooleanField(default=False)
    daily_update = models.BooleanField(null=False, default=False)
    der = models.DateField(null=True, blank=True)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)
    deleted_at = models.DateField(null=True)

    def __str__(self):
        return f'Nome: {self.payer_name} - CPF: {self.cpf}'

class PayerUpdate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE)
    situation = models.CharField(max_length=50)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]
        db_table = "payer_updates"
        verbose_name = "Atualização do Contribuinte"
        verbose_name_plural = "Atualizações do Contribuinte"


class Execution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(default=timezone.now)
    finished = models.BooleanField()
    finished_at = models.DateField()
