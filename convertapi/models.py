from django.db import models
from  authentication.models import User
CONVERT_STATUS_CHOICES = (
    ("start", 'start'),
    ("failed", 'failed'),
    ('completed','completed')
)


class Convert(models.Model):
    user = models.ForeignKey(User,null=True,blank=True,related_name="user_rel", on_delete=models.CASCADE)
    path = models.CharField(null=True,blank=True,max_length=1000)
    status =  models.CharField(choices=CONVERT_STATUS_CHOICES,blank=True,null=True,max_length=30)
    file_name = models.CharField(null=True,blank=True,max_length=1000)

    def __str__(self):
        return str(self.file_name)
