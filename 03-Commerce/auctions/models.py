from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=400, blank=True, null=True)
    price = models.FloatField()
    img = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    winner_id = models.IntegerField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.content)<=50:
            return f"{self.user}: {self.content}"
        else:
            return f"{self.user}: {self.content[0:50]}..."

    class Meta:
        ordering = ['-created']


class Bid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    
    class Meta:
        ordering = ['-price']
        #ordering = ['price']
