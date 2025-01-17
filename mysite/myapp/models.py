from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    file = models.FileField(upload_to='uploads')
    # if the user wants to upload any file like zip folder, pdf, image

    def __str__(self):
        return self.name
    
class OrderDetail(models.Model):
    customer_email = models.EmailField()
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_on=models.DateTimeField(auto_now_add=True)