from django import forms
from .models import Client


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class ClientRegistrationForm(forms.ModelForm):
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
        first_name = cd['first_name']
        last_name = cd['last_name']
        type = cd['type']

        if password != password2:
            raise forms.ValidationError("Passwords did not match")

        if email and Client.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError("This email address is already in use.")

        if username and Client.objects.filter(username=username).exclude(email=email).count():
            raise forms.ValidationError("Username already exists")

