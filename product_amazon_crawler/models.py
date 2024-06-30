from djongo import models

class AmazonDataScrapCollection(models.Model):
    _id = models.ObjectIdField()
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now=True)