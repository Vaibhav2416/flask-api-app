from django.db import models

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    quantity=models.IntegerField()
    
    def __str__(self):
        return self.name
    
class Review(models.Model):
    text=models.CharField(max_length=100)
    rating=models.IntegerField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name