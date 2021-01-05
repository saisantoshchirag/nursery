from django.contrib import admin
from .models import Plants,Order,Nursery,Ordered
# Register your models here.
admin.site.register(Plants)
admin.site.register(Order)
admin.site.register(Nursery)
admin.site.register(Ordered)