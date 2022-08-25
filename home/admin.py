from django.contrib import admin

# Register your models here.
from .models import Product, Contact, Order, Category, Customer

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)