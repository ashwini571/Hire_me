from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Certifications, Project, Education, Client
from .forms import UserProfileForm, EducationForm, ProjectForm, CertificationsForm
import os
from HireMe import settings


@login_required(login_url='/login')
def change_basic_user_data(request):
    if request.method == 'POST':
        user_instance = Client.objects.get(username=request.user.username)

        first_name = request.POST.get('first_name')
        if first_name:
            user_instance.first_name = first_name

        last_name = request.POST.get('last_name')
        if last_name:
            user_instance.last_name = last_name

        if request.FILES.get('image'):  # Delete previous and rename image

            if user_instance.profile_image:  # Delete previous image. Make profile_image None
                os.remove(os.path.join(settings.MEDIA_ROOT, user_instance.profile_image.name))
                user_instance.profile_image = None
                user_instance.save()
                print('Deleted Previous image. \n Now saving new')

            format_name = request.FILES.get('image').name.split('.')
            request.FILES.get('image').name = "{}.{}".format(user_instance.username, format_name[1])  # Rename Uploaded file
            user_instance.profile_image = request.FILES.get('image')
            user_instance.save()
        user_instance.save()
        return redirect('accounts:home')

    else:
        return render(request, 'dummy_form.html')


@login_required(login_url='/login')
def create_user_profile_view(request):
    if request.method == 'POST':
        try:
            get_object_or_404(UserProfile, user=request.user)
            return HttpResponse("Profile already exists")
        except:
            form = UserProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.resume = request.FILES.get('resume')
                profile.save()
                return redirect('accounts:add_education')
            else:
                print(form.errors)
                context = {'title': 'Profile', 'form': form}
                return render(request, 'userProfileForm.html', context=context)
    else:
        form = UserProfileForm()
        return render(request, 'userProfileForm.html', context={'title': 'Profile', 'form': form})


@login_required(login_url='/login')
def add_education_view(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.profile = UserProfile.objects.get(user=request.user)
            edu.save()
            return redirect('accounts:add_project')
        else:
            print(form.errors)
            context = {'title': 'Profile', 'form': form}
            return render(request, 'educationAdditionForm.html', context=context)
    else:
        form = EducationForm()
        return render(request, 'educationAdditionForm.html', context={'title': 'Add Education', 'form': form})


@login_required(login_url='/login')
def add_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = UserProfile.objects.get(user=request.user)
            project.save()
            return redirect('accounts:add_certificate')
        else:
            print(form.errors)
            context = {'title': 'Project', 'form': form}
            return render(request, 'projectAdditionForm.html', context=context)
    else:
        form = ProjectForm()
        return render(request, 'projectAdditionForm.html', context={'title': 'Project', 'form': form})


@login_required(login_url='/login')
def add_certificate_view(request):
    if request.method == 'POST':
        form = CertificationsForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.profile = UserProfile.objects.get(user=request.user)
            cert.save()
            return redirect('accounts:home')
        else:
            print(form.errors)
            context = {'title': 'Certificate', 'form': form}
            return render(request, 'certfificateAdditionForm.html', context=context)
    else:
        form = CertificationsForm()
        return render(request, 'certfificateAdditionForm.html', context={'title': 'Certificate', 'form': form})