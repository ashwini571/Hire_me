from django.shortcuts import render, redirect
from django.contrib import auth
from django.db.models import Count ,Q
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, ClientRegistrationForm
from .models import JobApplication, Client, OrgProfile, Contact, AppliedJobs, UserProfile
from .models import JobApplication, Client, OrgProfile, Contact, AppliedJobs
from django.shortcuts import get_list_or_404, get_object_or_404
from .utils import create_job_id
from .decorators import normal_user_required, company_required, ajax_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from feed.utils import create_action
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



def home(request):
    all_jobs = JobApplication.objects.all().order_by('-pk')[:5]
    return render(request, 'index.html', {'title': "Home", 'jobs': all_jobs})


@login_required(login_url='/login')
def dashboard(request):
    usr = request.user

    if usr.is_organisation():
        org = get_object_or_404(OrgProfile, user=usr)
        jobs = JobApplication.objects.filter(org=org).values()
        return render(request, 'company_dash.html', context={'user': usr, 'jobs': jobs})
    else:
        edu = usr.profile.education.all()
        pro = usr.profile.projects.all()
        certs = usr.profile.certificates.all()
        return render(request, 'user_dash.html', context={'title': usr.first_name, 'education': edu,
                                                          'projects': pro, 'certificates': certs})


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def logout_view(request):
    auth.logout(request)
    return redirect('accounts:home')


@login_required(login_url='/login')
@company_required
def get_org_profile(request, id):
    org = OrgProfile.objects.get(user=Client.objects.get(username=id))
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
        create_action(request.user, "posted a new job", 'new_job', application)
        return render(request, 'post_job.html', context={'messages': msg})
    else:
        print(0)
        return render(request, 'post_job.html')


@login_required(login_url='/login')
def view_profile(request, username):
    try:
        u = get_object_or_404(Client, username=username)
        if u.is_individual():
            edu = u.profile.education.all()
            pro = u.profile.projects.all()
            certs = u.profile.certificates.all()
            print(username)
        else:
            jobs = JobApplication.objects.filter(org=u.profile_org).values()
        # if user search for himself , is redirected to his dashboard
        if username == request.user.username:
            return redirect('accounts:dashboard')
        elif u.is_organisation():
            return render(request, 'company_public_profile.html',
                          context={'title': u.username, 'user': u, 'jobs': jobs})
        else:
            return render(request, 'user_public_profile.html', context={'title': u.username, 'u': u, 'education': edu,
                                                                        'projects': pro, 'certificates': certs})
    except:
        return HttpResponse("No Such user exists")


def view_job(request, id):
    user = request.user
    job = JobApplication.objects.get(id=id)
    job_tags_ids = job.req_skills.values_list('id', flat=True)
    print(job_tags_ids)
    similar_jobs = JobApplication.objects.filter(req_skills__in=job_tags_ids).exclude(id=id)
    similar_jobs = similar_jobs.annotate(same_req_skills=Count('req_skills')).order_by('-same_req_skills')[:4]

    if request.method == 'POST':
        new_app = AppliedJobs()
        new_app.id = create_job_id(5)
        new_app.job = job
        new_app.user = user.profile
        new_app.date_responded = now()
        new_app.save()
        create_action(request.user, 'applied to a job', 'applied_to_job', new_app)

        return render(request, 'view_single_job.html',
                      context={'job': job, 'user': user, 'application': new_app, 'similar_jobs': similar_jobs})
    else:
        try:
            application = AppliedJobs.objects.filter(job=job).filter(user=user.profile)
        except:
            application = None

        if application:
            application = application[0]

        if request.user.is_authenticated:
            if user.is_organisation():
                print(1)
                return render(request, 'view_single_job.html',
                              context={'job': job, 'user': user, 'similar_jobs': similar_jobs})
            else:
                print(9)
                return render(request, 'view_single_job.html',
                              context={'job': job, 'user': user, 'application': application,
                                       'similar_jobs': similar_jobs})
        else:
            error = ["You must login first!"]
            return render(request, 'login.html', context={'errors': error})


# Dashboard of person to which user wants to follow or unfollow
# @login_required
# def user_detail(request, username):
#     user = get_object_or_404(Client, username=username, is_active=True)
#     return render(request, 'detail.html', {'section': 'people', 'user': user})


# List of recommended users
# @login_required
# def recommended_user_list(request):
#     users = Client.objects.filter(is_active=True, type='user')
#     return render(request, 'list.html', {'section': 'people', 'users': users})


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
                create_action(request.user, "started following", 'follow', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except Client.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})


@login_required(login_url='/login')
def see_add_response(request, app_id):
    application = AppliedJobs.objects.filter(id=app_id)
    application = application[0]
    if request.method == 'POST' and request.user.is_organisation():
        application.status = True
        application.response = request.POST.get('text')
        application.save()
        create_action(request.user, "responded to your job application", 'job_response', application)
        message = ["Response Sent!"]
        return render(request, 'response.html', context={'messages': message, 'application': application})
    else:
        return render(request, 'response.html', context={'application': application})


# For getting no of common elements in two lists
def intersection(lst1, lst2):
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return len(lst3)


@login_required(login_url='/login')
@company_required
def manage_candidates(request, job_id):
    job = JobApplication.objects.filter(id=job_id)
    job_tags_ids = job[0].req_skills.values_list('id', flat=True)
    print(job_tags_ids)
    applications = AppliedJobs.objects.filter(job__in=job)
    for app in applications:
        common_skills = intersection(job_tags_ids,app.user.skills.values_list('id', flat=True))
        app.match = (common_skills/len(job_tags_ids))*100

    return render(request, 'manage_candidates.html', context={'job': job[0], 'applications': applications})


@login_required(login_url='/login')
def manage_jobs(request):
    if request.user.is_organisation():
        jobs = JobApplication.objects.filter(org=request.user.profile_org)
        return render(request, 'manage_jobs.html', context={'jobs': jobs})
    else:
        jobs = AppliedJobs.objects.filter(user=request.user.profile)
        return render(request, 'manage_jobs_user.html', context={'applications': jobs})


def browse_companies(request, letter):
    companies = Client.objects.filter(first_name__startswith=letter).filter(type='org')
    print(companies)
    return render(request, 'browse_companies.html', context={'companies': companies})


# search views
def search_people(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        # this is for search with OR
        people = Client.objects.filter(Q(first_name__icontains=key)|Q(username__icontains=key)|Q(last_name__icontains=key))
    else:
        people=None
    return render(request, 'search_people.html', context={'people':people})


def search_job(request):
    # if request.method == 'GET':
        if request.GET.get('key'):
            key = request.GET.get('key')
        else:
            key = " "
        jobs = JobApplication.objects.filter(Q(title__icontains=key)|Q(type__icontains=key)|Q(category__icontains=key)|Q(location__icontains=key)|Q(org__user__username__contains=key))
        paginator = Paginator(jobs, 2)  # Show 15 issues per page
        page = request.GET.get('page', 1)
        try:
            jobs = paginator.get_page(page)
        except PageNotAnInteger:
            jobs = paginator.get_page(1)
        except EmptyPage:
            jobs = paginator.get_page(paginator.num_pages)

        print(jobs)
    # else:
    #     jobs = None

        return render(request, 'search_job.html', context={'jobs':jobs})
