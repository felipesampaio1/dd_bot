import uuid

from django.utils import timezone
from taxpayers import models

class Config(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(default=timezone.now)
    execution_period = models.IntegerField()
    finished = models.BooleanField()
    finished_at = models.DateField()