from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import JobApplication

def home(request):
    all_jobs = JobApplication.objects.all()
    return render(request, 'index.html', {'title': "Home",'jobs':all_jobs})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    if request.method == 'POST':
        print("hola")
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('accounts:home')
            else:
                context = {'form': form, 'messages': ['Incorrect Username or password', ], 'title': "ERROR"}
        else:
            context = {'form': form, 'messages': ['Invalid Form', ], 'title': "ERROR"}
    else:
        context = {'form': LoginForm(), 'title': 'login'}
    return render(request, 'login.html', context=context)

@login_required
def logout_view(request):
        auth.logout(request)
        return redirect('accounts:home')

