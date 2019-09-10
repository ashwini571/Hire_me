from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, ClientRegistrationForm
from .models import JobApplication, Client, OrgProfile, Contact
from django.shortcuts import get_list_or_404, get_object_or_404
import random
from .decorators import normal_user_required, company_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest


def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap


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
                context = {'form': form, 'errors': ['Incorrect Username or password', ], 'title': "ERROR"}
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
    return render(request, 'company_profile.html', context=context)


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
        id = create_job_id(4)
        application.id = id
        application.org = request.user.profile_org
        application.title = request.POST.get('title')
        application.type = request.POST.get('type')
        application.category = request.POST.get('category')
        application.salary = request.POST.get('salary')
        application.location = request.POST.get('location')
        application.descr = request.POST.get('about')
        req_skills = request.POST.get('req_skills')
        req_skills = req_skills.split(',')

        for skill in req_skills:
            application.req_skills.add(skill)
        msg = ["Job Added, Job Id is:" + str(id)]
        application.save()
        return render(request,'post_job.html',context={'messages':msg})
    else:
        print(0)
        return render(request, 'post_job.html')


def create_job_id(digits):
    lower = 10 ** (digits - 1)
    upper = 10 ** digits - 1
    uid = random.randint(lower, upper)

    # check if Quiz already exists if not, return id
    try:
        job_applications = JobApplication.objects.get(job_id=uid)
    except:
        job_applications = None

    if not job_applications:
        return uid
    else:
        create_quiz_id(digits)  # If uid already exists recreate uid


def view_job(request, id):
    user = request.user
    job = JobApplication.objects.get(id=id)
    try:
        application = AppliedJobs.objects.filter(id=id).filter(user=user)
    except:
        application = None
    print(application)

    if request.user.is_organisation:
        return render(request, 'view_single_job.html',context={'job':job, 'user': user})
    else:
        return render(request, 'view_single_job.html', context={'job': job, 'user': user,'application':application})


# Dashboard of person to which user wants to follow or unfollow
@login_required
def user_detail(request, username):
    user = get_object_or_404(Client, username=username, is_active=True)
    return render(request, 'detail.html', {'section': 'people', 'user':user})


# List of recommended users
@login_required
def user_list(request):
    users = Client.objects.filter(is_active=True)
    return render(request, 'list.html', {'section': 'people', 'users': users})


# Follow Function
@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = Client.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except Client.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})