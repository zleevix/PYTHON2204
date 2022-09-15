from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, Promotion
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Promotion)