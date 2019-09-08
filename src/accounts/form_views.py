from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Certifications, Project, Education
from .forms import UserProfileForm, EducationForm, ProjectForm, CertificationsForm


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