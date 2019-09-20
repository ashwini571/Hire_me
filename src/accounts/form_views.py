from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Certifications, Project, Education, Client, OrgProfile
from .forms import UserProfileForm, EducationForm, ProjectForm, CertificationsForm
import os
from .resume_parser import extract_skills_func
from HireMe import settings
from django.contrib import auth, messages
from .decorators import normal_user_required, company_required


@login_required(login_url='/login')
def password_change_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if new_password1 == new_password2:
            user = auth.authenticate(username=request.user.username, password=old_password)
            if user == request.user:
                user_instance = Client.objects.get(username=user.username)
                user_instance.set_password(new_password1)
                user_instance.save()
                messages.success(request, 'Your password was successfully updated!')
                return redirect('accounts:login')
            else:
                return HttpResponse("Old password is incorrect")
        else:
            return HttpResponse("Passwords do not match")
    else:
        return redirect('accounts:settings')


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
            print("Image Found")
            if user_instance.profile_image:  # Delete previous image. Make profile_image None
                os.remove(os.path.join(settings.MEDIA_ROOT, user_instance.profile_image.name))
                user_instance.profile_image = None
                user_instance.save()
                print('Deleted Previous image. \n Now saving new')

            format_name = request.FILES.get('image').name.split('.')
            request.FILES.get('image').name = "{}.{}".format(user_instance.username, format_name[-1])
            print("renamed Image")  # Rename Uploaded file
            user_instance.profile_image = request.FILES.get('image')

        user_instance.save()
        return redirect('accounts:settings')

    else:
        return render(request, 'user_data_form.html')


@login_required(login_url='/login')
@normal_user_required
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

                if request.FILES.get('resume'):  # Delete previous and rename image
                    print("Resume Found")
                    if profile.resume:  # Delete previous image. Make profile_image None
                        os.remove(os.path.join(settings.MEDIA_ROOT, profile.resume.name))
                        profile.resume = None
                        profile.save()
                        print('Deleted Previous Resume. \n Now saving new')

                    format_name = request.FILES.get('resume').name.split('.')
                    request.FILES.get('resume').name = "{}-{}.{}".format(request.user.username,
                                                                         "resume", format_name[-1])
                    print("renamed Image")  # Rename Uploaded file
                    profile.resume = request.FILES.get('resume')

                profile.save()
                skills = extract_skills_func(profile.resume.path)
                profile.skills.clear()
                for skill in skills:
                    print(skill)
                    profile.skills.add(skill)
                profile.save()
                return redirect('accounts:skills_upload')
            else:
                print(form.errors)
                context = {'title': 'Profile', 'form': form}
                return render(request, 'userProfileForm.html', context=context)
    else:
        form = UserProfileForm()
        return render(request, 'userProfileForm.html', context={'title': 'Profile', 'form': form})


@login_required(login_url='/login')
@normal_user_required
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
@normal_user_required
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
@normal_user_required
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


@login_required(login_url='/login')
@normal_user_required
def edit_user_profile(request):
    profile = request.user.profile
    if profile is None:
        return redirect('accounts:create_user_profile')
    if request.method == 'POST':
        skills = request.POST.get('skills')
        lang = request.POST.get('languages')
        sex = request.POST.get('gender') if request.POST.get('gender') else profile.gender
        about = profile.about if not request.POST.get('about') else request.POST.get('about')
        skills = skills.split(',')

        # first we will clear all previous tags
        profile.skills.clear()
        for skill in skills:
            print(skill)
            profile.skills.add(skill)
        profile.languages = lang
        profile.gender = sex
        profile.about = about

        if request.FILES.get('resume'):  # Delete previous and rename image
            print("Resume Found")
            if profile.resume:  # Delete previous image. Make profile_image None
                os.remove(os.path.join(settings.MEDIA_ROOT, profile.resume.name))
                profile.resume = None
                profile.save()
                print('Deleted Previous Resume. \n Now saving new')

            format_name = request.FILES.get('resume').name.split('.')
            request.FILES.get('resume').name = "{}-{}.{}".format(request.user.username,
                                                                 "resume", format_name[-1])
            print("renamed Image")  # Rename Uploaded file
            profile.resume = request.FILES.get('resume')

        profile.save()
    return redirect('accounts:settings')


@login_required()
@company_required
def create_edit_company_profile(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        about = request.POST.get('about')
        mis_vis = request.POST.get('mis_vis')
        why_us = request.POST.get('why_us')
        fields = request.POST.get('fields')
        teams = request.POST.get('teams')
        user = request.user
        try:
            profile = get_object_or_404(OrgProfile, user=request.user)
            profile.about = about
            profile.mis_vis = mis_vis
            profile.why = why_us
            profile.teams = teams
            fields = fields.split(',')
            profile.area_of_work.clear()
            for field in fields:
                print(field)
                profile.area_of_work.add(field)

            if image:
                if user.profile_image:
                    os.remove(os.path.join(settings.MEDIA_ROOT, user.profile_image.name))
                    user.profile_image = None
                    user.save()
                    print('Deleted Previous Image. \n Now saving new')

                format_name = request.FILES.get('image').name.split('.')
                request.FILES.get('image').name = "{}-{}.{}".format(request.user.username,
                                                                    "company", format_name[-1])
                print("renamed Image")  # Rename Uploaded file
                user.profile_image = request.FILES.get('image')
                user.save()

            profile.save()
            return redirect('accounts:settings')

        except:
            profile = OrgProfile.objects.create(user=request.user, verification=True, about=about,
                                                mis_vis=mis_vis, why=why_us, teams=teams)
            profile.save()
            if image:
                user.profile_image = image
                user.save()
            fields = fields.split(',')
            for field in fields:
                print(field)
                profile.area_of_work.add(field)
            return redirect('accounts:settings')

    else:
        return redirect('accounts:settings')


@login_required(login_url='/login')
@normal_user_required
def skills_upload(request):
    if request.method == 'POST':
        profile = request.user.profile
        skills = request.POST.get('skills')
        skills = skills.split(',')
        profile.skills.clear()
        for skill in skills:
            print(skill)
            profile.skills.add(skill)
        profile.save()
        return redirect('accounts:add_education')
    else:
        return render(request, 'skills.html', context={'user': request.user})
