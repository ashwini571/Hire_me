from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, ClientRegistrationForm
from .models import JobApplication, Client


def home(request):
    all_jobs = JobApplication.objects.all()[:5]
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


def get_org_profile(request, id):
    org = OrgProfile.objects.get(user = Client.objects.get(username=id))
    if request.user.username == id:
        context = {'add_job': 1, 'org_profile': org}
    else:
        context = {'org_profile': org}
    return render(request, 'company_profile', context=context)


def registration_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        context = {'title': 'Sign Up', 'form': form}
        if form.is_valid():

            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            email = cd['email']
            first_name = cd['first_name']
            last_name = cd['last_name']
            user_type = cd['type']

            user = Client.objects.create(username=username, email=email, first_name=first_name,
                                         last_name=last_name, type=user_type)
            user.set_password(password)
            user.save()

            usr = auth.authenticate(username=username, password=password)
            auth.login(request, usr)
            return redirect('accounts:home')

        else:
            print('errors')
            return render(request, 'reg_form.html', context=context)
    else:
        form = ClientRegistrationForm()
        return render(request, 'reg_form.html', context={'title': 'Sign Up', 'form': form})

