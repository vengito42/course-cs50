from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Comment, Bid, Category

# Register your models here.
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Category)
