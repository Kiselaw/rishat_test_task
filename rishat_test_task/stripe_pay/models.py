from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class Discount(models.Model):
    # order = models.ManyToManyField(Order)
    amount = models.PositiveIntegerField(unique=True, validators=[MaxValueValidator(90)])

    def __str__(self):
        return f'{self.amount}% discount'

class Tax(models.Model):
    # order = models.ManyToManyField(Order)
    amount = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(10), MaxValueValidator(25)])

    def __str__(self):
        return f'{self.amount}% tax'

class Order(models.Model):
    items = models.ManyToManyField(Item)
    has_discount = models.BooleanField()
    discounts = models.ManyToManyField(Discount)
    taxes = models.ManyToManyField(Tax)
