from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import Truncator


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='topics')
    Publisher = models.ForeignKey(User,on_delete=models.CASCADE,related_name='topics')

    def __str__(self):
        return self.subject


class Blog(models.Model):
    Blog_Text = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='posts')
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name='+')
    Image = models.ImageField(upload_to='static/media', blank=True, max_length=100)

    def __str__(self):
        return self.Blog_Text
