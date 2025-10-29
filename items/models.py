from django.db import models

# Create your models here.

class Item(models.Model):
    articul = models.CharField(max_length=10)
    name = models.TextField(max_length=100)
    dimension = models.CharField(max_length=10)
    price = models.IntegerField()
    supplier = models.CharField(max_length=50)
    prod = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    discount = models.IntegerField()
    count = models.IntegerField()
    description = models.TextField()
    photo = models.CharField(max_length=100)

    def to_dict(self):
        return {
            'name': self.name,
            'articul': self.articul,
            'id': self.id
        }
