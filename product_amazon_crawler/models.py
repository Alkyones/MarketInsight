from django.db import models
from enum import Enum
from django.contrib.auth.models import User

class ScrapRequestStatus(Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


    
class ScrapRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    country_code = models.CharField(max_length=2)
    request_date = models.DateTimeField(auto_now_add=True)
    request_reason = models.CharField(max_length=255, default='Request reason not provided.')
    status = models.CharField(max_length=10, default=ScrapRequestStatus.PENDING.value)

    def __str__(self):
        return f"{self.pk} - {self.user} - {self.country_code} - {self.request_date.strftime('%d-%m-%Y')} - {self.request_reason} - {self.status}"
    class Meta:
        verbose_name = "Scrap Request"
        verbose_name_plural = "Scrap Requests"

    def __repr__(self):
        return f"ScrapRequest(pk={self.pk}, user={self.user}, country_code={self.country_code}, request_date={self.request_date}, request_reason={self.request_reason}, status={self.status})"
    
class AmazonDataScrapCollection(models.Model):
    request = models.ForeignKey(ScrapRequest, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}  - {self.user}  - {self.created_at.strftime('%d-%m-%Y %H:%M:%S')}"
    class Meta:
        verbose_name = "Amazon Data Scrap Collection"
        verbose_name_plural = "Amazon Data Scrap Collections"

    def __repr__(self):
        return f"AmazonDataScrapCollection(pk={self.pk}, request={self.request}, user={self.user}, data={self.data})"

    def get_request(self):
        return self.request


class AmazonDataScrapCountry(models.Model):
    country_code = models.CharField(max_length=2, unique=True)
    country_name = models.CharField(max_length=100)
    url = models.URLField()
    navbar_xpath = models.CharField(max_length=255, default='')
    link_xpath = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"{self.country_code} - {self.country_name} - {self.url}"

    class Meta:
        verbose_name = "Amazon Data Scrap Country"
        verbose_name_plural = "Amazon Data Scrap Countries"

    def __repr__(self):
        return f"AmazonDataScrapCountry(pk={self.pk}, country_code={self.country_code}, country_name={self.country_name}, url={self.url})"