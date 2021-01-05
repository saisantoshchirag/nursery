from django.db import models
from django.contrib.auth.models import User
# Create your models here.
choices = (
    ('Nursery','Nurser'),
    ('User','User')
)
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    type = models.CharField(max_length=20,choices=choices,default='User')