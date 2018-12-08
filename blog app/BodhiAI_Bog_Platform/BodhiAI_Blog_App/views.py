from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from .models import Category,Topic,Blog

def home(request):
    categories =  Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

def category_topics(request, pk):
    category = get_object_or_404(Category, pk=pk)
    topics = category.topics.order_by('-last_updated')
    return render(request, 'topics.html', {'category': category, 'topics': topics})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, category__pk=pk, pk=topic_pk)
    blog =  Blog.objects.all()
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic,"blog":blog})