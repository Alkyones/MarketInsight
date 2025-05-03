from djongo import models
from enum import Enum
from django.contrib.auth.models import User

class ScrapRequestStatus(Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


    
class ScrapRequest(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    country_code = models.CharField(max_length=2)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default=ScrapRequestStatus.PENDING.value)
class AmazonDataScrapCollection(models.Model):
    _id = models.ObjectIdField()
    request = models.ForeignKey(ScrapRequest, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now=True)
    
    