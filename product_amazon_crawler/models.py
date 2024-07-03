from djongo import models
from enum import Enum

class AmazonDataScrapCollection(models.Model):
    _id = models.ObjectIdField()
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now=True)
    
class ScrapRequestStatus(Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class ScrapRequest(models.Model):
    _id = models.ObjectIdField()
    country_code = models.CharField(max_length=2)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default=ScrapRequestStatus.PENDING.value)