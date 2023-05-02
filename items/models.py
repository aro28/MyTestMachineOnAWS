from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Item(models.Model):
    title = models.CharField(max_length=20)
    price = models.FloatField()
    desc = models.CharField(max_length=20)
    # image = models.ImageField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.title