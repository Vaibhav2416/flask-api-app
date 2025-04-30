from django.contrib import admin
from .models import Product,Review
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','quantity']

class ReviewAdmin(admin.ModelAdmin):
    list_display=['rating','product']

admin.site.register(Product,ProductAdmin)
admin.site.register(Review,ReviewAdmin)