from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.urls import reverse
#from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import UserRegistrationForm
# Create your views here.

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            messages.error(request,'Bad Username or Password!')
            #return HttpResponseRedirect(reverse('Accounts:login')
    return render(request,'accounts\login.html')

def logout_page(request):
    logout(request)
    return redirect('home')

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            user = User.objects.create_user(username, email=email, password=password1)
            messages.success(request,'Thanks for registering {}'.format(user.username))
            return redirect('Accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request,'accounts\\register.html',{'form':form})
