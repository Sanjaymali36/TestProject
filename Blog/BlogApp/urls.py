"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'BlogApp'
urlpatterns = [
    path('list/', views.blog_list,name='list'),
    path('add/', views.add_blog,name='add'),
    path('edit_blog/<int:blog_id>/', views.blog_edit,name='edit_blog'),
    path('delete/blog/<int:blog_id>/', views.delete_blog,name='delete_confirm_blog'),
    path('edit_blog/<int:blog_id>/choice/add/', views.add_choice,name='add_choice'),
    path('edit/choice/<int:choice_id>/', views.edit_choice,name='edit_choice'),
    path('delete/choice/<int:choice_id>/', views.delete_choice,name='delete_confirm_choice'),
    path('details/<int:blog_id>/', views.blog_details,name='detail'),
    path('details/<int:blog_id>/vote/', views.blog_like,name='vote'),
]
