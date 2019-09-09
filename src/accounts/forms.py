from django import forms
from .models import Client, UserProfile, Education, Project, Certifications


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class ClientRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'type']

    def clean(self):
        cd = self.cleaned_data
        username = cd['username']
        password = cd['password']
        password2 = cd['password2']
        email = cd['email']
        if password != password2:
            raise forms.ValidationError("Passwords did not match")

        if email and Client.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError("This email address is already in use.")

        if username and Client.objects.filter(username=username).exclude(email=email).count():
            raise forms.ValidationError("Username already exists")


class UserProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=UserProfile.SEXES)

    class Meta:
        model = UserProfile
        fields = ['gender', 'about', 'skills', 'resume', 'languages']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 4}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'field_of_study', 'start_year', 'end_year', 'is_studying', 'description', 'grade']
        widgets = {
            'is_studying': forms.CheckboxInput(attrs={'class': 'col-xl-1'}),
            'start_year': forms.DateInput(attrs={'class': 'col-xl-4 date-picker'}),
            'end_year': forms.DateInput(attrs={'class': 'col-xl-4 date-picker'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'start_date', 'end_date', 'is_active', 'associated_with', 'project_URL', 'description']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'col-xl-1'}),
            'start_date': forms.DateInput(attrs={'class': 'col-xl-4 date-picker'}),
            'end_date' : forms.DateInput(attrs={'class': 'col-xl-4 date-picker'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CertificationsForm(forms.ModelForm):
    class Meta:
        model = Certifications
        fields = ['name', 'issuing_organisation', 'issue_date', 'credential_ID', 'credential_URL']
        widgets = {
            'issue_date': forms.DateInput(attrs={'class': 'col-xl-4 date-picker'}),
        }
