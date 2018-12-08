from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Category,Topic,Blog

admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Topic)