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
    request_reason = models.CharField(max_length=255, default='Request reason not provided.')
    status = models.CharField(max_length=10, default=ScrapRequestStatus.PENDING.value)
class AmazonDataScrapCollection(models.Model):
    _id = models.ObjectIdField()
    request = models.ForeignKey(ScrapRequest, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self._id)
    class Meta:
        verbose_name = "Amazon Data Scrap Collection"
        verbose_name_plural = "Amazon Data Scrap Collections"
        
    def __repr__(self):
        return f"AmazonDataScrapCollection(_id={self._id}, request={self.request}, user={self.user}, data={self.data})"
   
    def get_request(self):
        request = ScrapRequest.objects.get(_id=self.request._id)
        return request

            
    
    