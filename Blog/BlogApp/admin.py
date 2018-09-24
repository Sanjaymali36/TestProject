from django.contrib import admin
from .models import BlogModel,Choice,Vote
# Register your models here.
admin.site.register(BlogModel)
admin.site.register(Choice)
admin.site.register(Vote)
