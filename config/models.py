import uuid

from django.db import models


class Config(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_at = models.DateField(null=True)
    execution_period = models.IntegerField(
        help_text="Tempo de execução automática (em minutos)"
    )
    autenticado = models.BooleanField(
        default=False, help_text="Define se o sistema está autenticado"
    )
    finished = models.BooleanField()
    finished_at = models.DateField()
