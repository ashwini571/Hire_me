from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .models import UserProfile, Certifications, Project, Education
from .forms import UserProfileForm, EducationForm, ProjectForm, CertificationsForm


@login_required(login_url='/login')
def create_user_profile_view(request):
    if request.method == 'POST':
        pass
    else:
        form = UserProfileForm()
        return render(request, 'userProfileForm.html', context={'title': 'Profile', 'form': form})


@login_required(login_url='/login')
def add_education_view(request):
    if request.method == 'POST':
        pass
    else:
        form = EducationForm()
        return render(request, 'educationAdditionForm.html', context={'title': 'Add Education', 'form': form})


@login_required(login_url='/login')
def add_project_view(request):
    if request.method == 'POST':
        pass
    else:
        form = ProjectForm()
        return render(request, 'projectAdditionForm.html', context={'title': 'Profile', 'form': form})


@login_required(login_url='/login')
def add_certificate_view(request):
    if request.method == 'POST':
        pass
    else:
        form = CertificationsForm()
        return render(request, 'certfificateAdditionForm.html', context={'title': 'Profile', 'form': form})