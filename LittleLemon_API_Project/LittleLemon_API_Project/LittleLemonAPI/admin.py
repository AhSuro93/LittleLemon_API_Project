from django.contrib import admin
from .models import Category, MenuItem ,OrderItem , Order
# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(OrderItem)
admin.site.register(Order)
