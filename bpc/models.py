import uuid
from django.db import models
from django.utils import timezone
from taxpayers.models import Payer

class BpcExecution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE)
    execution_date = models.DateTimeField(default=timezone.now)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)

class BpcAtendimento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    execution = models.ForeignKey(BpcExecution, on_delete=models.CASCADE)

    # Campos do Atendimento
    protocolo = models.CharField(max_length=50, blank=True)
    servico = models.CharField(max_length=200, blank=True)
    situacao = models.CharField(max_length=100, blank=True)
    unidade_responsavel = models.CharField(max_length=200, blank=True)
    unidade_protocolo = models.CharField(max_length=200, blank=True)

    # Campos do Protocolo
    canal_requerente = models.CharField(max_length=100, blank=True)
    data_solicitacao = models.DateTimeField(null=True)
    data_protocolo = models.DateTimeField(null=True)
    solicitante = models.CharField(max_length=200, blank=True)
    cpf_solicitante = models.CharField(max_length=14, blank=True)

    # Campos do Requerente
    nome_requerente = models.CharField(max_length=200, blank=True)
    cpf_requerente = models.CharField(max_length=14, blank=True)
    data_nascimento = models.DateField(null=True)
    email = models.EmailField(max_length=200, blank=True)
    telefone_fixo = models.CharField(max_length=20, blank=True)
    celular = models.CharField(max_length=20, blank=True)
    acompanha_processo = models.BooleanField(default=False)

    # Campos adicionais e anexos como JSONField
    campos_adicionais = models.JSONField(default=dict)
    anexos = models.JSONField(default=dict)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_solicitacao']
        verbose_name = 'Atendimento BPC'
        verbose_name_plural = 'Atendimentos BPC'