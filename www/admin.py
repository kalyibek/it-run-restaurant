from django.contrib import admin
from . import models

admin.site.register(models.Food)
admin.site.register(models.Drink)
admin.site.register(models.Order)
admin.site.register(models.OrderFood)
admin.site.register(models.OrderDrink)
