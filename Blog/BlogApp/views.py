from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse
from .forms import BlogForm, EditBlogForm, EditChoiceForm
from .models import BlogModel,Choice,Vote
import datetime
# Create your views here.
@login_required
def blog_list(request):
    search_term = ''
    info = BlogModel.objects.all()
    if 'text' in request.GET:
        info = info.order_by('text')
    if 'pub_date' in request.GET:
        info = info.order_by('-pub_date')
    if 'num_votes' in request.GET:
        info = info.annotate(Count('vote')).order_by('-vote__count')
    my_blog = BlogModel.objects.filter(owner=request.user)
    #my_blog_list = request.user.blog_set.all()
    if 'search' in request.GET:
        search_term = request.GET['search']
        info = info.filter(text__icontains=search_term)
    paginator  = Paginator(info,5)
    page = request.GET.get('page')
    info = paginator.get_page(page)
    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page',True) and get_dict_copy.urlencode()
    content = {'info':info,'params':params,'search_term':search_term}
    return render(request,'blog/blog.html',content)

@login_required
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        form.is_valid()
        new_blog = form.save(commit=False)
        new_blog.pub_date = datetime.datetime.now()
        new_blog.save()
        new_choice1 = Choice(blog=new_blog,choice_text=form.cleaned_data['choice1']).save()
        new_choice2 = Choice(blog=new_blog,choice_text=form.cleaned_data['choice2']).save()
        messages.success(request,
                                'Text and Choice are Added!',
                                extra_tags='alert alert-success alert-dismissible fade show')
        return redirect('BlogApp:list')
    else:
        form = BlogForm()
    context = {'form':form}
    return render(request,'blog/add.html',context)

@login_required
def blog_edit(request,blog_id):
    blog = get_object_or_404(BlogModel,id=blog_id)
    if request.user != blog.owner:
        return redirect('/')
    if request.method == 'POST':
        form = EditBlogForm(request.POST,instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request,'Blog Edit Successfully',
                                extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('BlogApp:list')
    else:
        form = EditBlogForm(instance=blog)
    return render(request,'blog/edit_blog.html',{'form':form,'blog':blog})

@login_required
def delete_blog(request,blog_id):
    blog = get_object_or_404(BlogModel,id=blog_id)
    if request.user != blog.owner:
        redirect('/')
    if request.method == 'POST':
        blog.delete()
        messages.success(request,'Blog Deleted Successfully',
                            extra_tags='alert alert-success alert-dismissible fade show')
        return redirect('BlogApp:list')
    return render(request,'blog/delete_confirm_blog.html',{'blog':blog})
@login_required
def add_choice(request, blog_id):
    blog = get_object_or_404(BlogModel,id=blog_id)
    if request.user != blog.owner:
        return redirect('/')
    if request.method == 'POST':
        form = EditChoiceForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.blog = blog
            new_choice.save()
            messages.success(request,'Choice Added Successfully',
                                extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('BlogApp:list')
    else:
        form = EditChoiceForm()
    return render(request,'blog/add_choice.html',{'form':form})

@login_required
def edit_choice(request,choice_id):
    choice = get_object_or_404(Choice, id = choice_id)
    blog = get_object_or_404(BlogModel,id=choice.blog.id)
    if request.user != blog.owner:
        return redirect('/')
    if request.method == 'POST':
        form = EditChoiceForm(request.POST,instance=choice)
        if form.is_valid():
            form.save()
            messages.success(request,'Choice Edited Successfully',
                                extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('BlogApp:list')
    else:
        form = EditChoiceForm(instance=choice)
    return render(request,'blog/add_choice.html',{'form':form,'edit_mode':True,'choice':choice})

@login_required
def delete_choice(request, choice_id):
        choice = get_object_or_404(Choice, id=choice_id)
        blog = get_object_or_404(BlogModel, id=choice.blog.id)
        if request.user != blog.owner:
            return redirect('/')
        if request.method == 'POST':
            choice.delete()
            messages.success(request,'Choice Deleted Successfully',
                                extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('BlogApp:list')
        return render(request,'blog/delete_choice_confirm.html',{'choice':choice})
@login_required
def blog_details(request,blog_id):
    blog = get_object_or_404(BlogModel,id=blog_id)
    user_can_vote = blog.user_can_vote(request.user)
    result = blog.get_result_dict()
    content = {'blog':blog,'user_can_vote':user_can_vote,'result':result}
    return render(request,'blog/blog_details.html',content)

@login_required
def blog_like(request, blog_id):
    blog = get_object_or_404(BlogModel, id=blog_id)
    if not blog.user_can_vote(request.user):
        messages.error(request,'Are you crazy? you already voted to this Blog!')
        return redirect('BlogApp:detail',blog_id=blog_id)
    choice_id = request.POST.get('choice')
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        new_vote = Vote(user = request.user, blog = blog, choice = choice)
        new_vote.save()
    else:
        messages.error(request,'No Choice Was Found!')
        return redirect('BlogApp:detail',blog_id=blog_id)
    return redirect('BlogApp:detail',blog_id=blog_id)
