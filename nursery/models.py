from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
# Create your models here.

class Nursery(models.Model):
    name = models.CharField(max_length=30,unique=True)
    state = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE)


class Plants(models.Model):
    name = models.CharField(max_length=30,unique=True)
    image = models.ImageField(upload_to='static/plants')
    price = models.IntegerField()
    nursery = models.ForeignKey(Nursery,on_delete=models.CASCADE)

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Plants,on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now=True)
    order_id = models.UUIDField(auto_created=True)
    is_purchased = models.BooleanField(default=False)
    cost = models.IntegerField()
    quantity = models.IntegerField()
    nursery = models.ForeignKey(Nursery,on_delete=models.CASCADE)

class Ordered(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ForeignKey(Order,on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now=True)
    nursery = models.ForeignKey(Nursery,on_delete=models.CASCADE)
    cost = models.IntegerField()
