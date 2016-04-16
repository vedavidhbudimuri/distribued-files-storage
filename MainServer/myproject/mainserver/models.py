
from django.db import models


class NodeStatus(models.Model):
    node_name = models.CharField(max_length=1000)
    ip = models.CharField(max_length=1000)
    status = models.BooleanField(default=True)
    
    