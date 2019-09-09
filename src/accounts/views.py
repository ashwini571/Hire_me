from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, ClientRegistrationForm
from .models import JobApplication, Client, OrgProfile
from django.shortcuts import get_list_or_404, get_object_or_404
from .decorators import normal_user_required, company_required


def home(request):
    all_jobs = JobApplication.objects.all()[:5]
    return render(request, 'index.html', {'title': "Home", 'jobs': all_jobs})


def dashboard(request):
    usr = request.user

    if usr.is_organisation():
        org = get_object_or_404(OrgProfile, user=usr)
        jobs = JobApplication.objects.filter(org=org).values()
        return render(request, 'company_dash.html', context={'user': usr, 'jobs':jobs})
    else:
        edu = usr.profile.education.all()
        pro = usr.profile.projects.all()
        certs = usr.profile.certificates.all()
        return render(request, 'user_dash.html', context={'title': usr.username, 'education': edu,
                                                          'projects': pro, 'certificates': certs})


def settings(request):
    usr = request.user
    if usr.is_organisation():
        return render(request, 'company_profile.html', context={'user': usr})
    else:
        return render(request, 'user_profile.html', context={'title': 'Settings'})


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


@company_required
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
            if usr.is_organisation():
                return redirect('accounts:settings')
            else:
                return redirect('accounts:create_user_profile')

        else:
            print('errors')
            return render(request, 'reg_form.html', context=context)
    else:
        form = ClientRegistrationForm()
        return render(request, 'reg_form.html', context={'title': 'Sign Up', 'form': form})


@login_required
@company_required
def post_job(request):
    if request.method == 'POST':
        print(1)
        application = JobApplication()
        application.org = request.user.profile_org
        application.title = request.POST.get('title')
        application.type = request.POST.get('type')
        application.category = request.POST.get('category')
        application.salary = request.POST.get('salary')
        application.location = request.POST.get('location')
        application.descr = request.POST.get('about')
        application.req_skills = request.POST.get('req_skills')
        application.save()
        return redirect('accounts:dashboard')
    else:
        print(0)
        return render(request, 'post_job.html')

