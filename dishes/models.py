from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
