from django import forms
from .models import User, Leaves
from django.contrib.auth import authenticate
from datetime import datetime, date


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise forms.ValidationError("Employee with this email already exists.")

        return email

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password must be same.")


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_email = User.objects.filter(email=email).exists()
        if not user_email:
            raise forms.ValidationError("This email has not been register")

        return email

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user_email = User.objects.filter(email=email).first()
        if user_email:
            username = user_email.username
            print(email, username, password)
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Email or Password is incorrect.')

        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        username = User.objects.filter(email=email).first().username
        user = authenticate(username=username, password=password)
        return user


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leaves
        fields = ('start', 'end', 'attachment')
        widgets = {
            'start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        start = self.cleaned_data['start']
        end = self.cleaned_data['end']
        today = date.today()
        if (start - today).days < 1:
            raise forms.ValidationError("Leave in past or on today is not possible.")
        if start > end:
            raise forms.ValidationError("Start date should not be after end date")
        if (end - start).days + 1 > 4:
            raise forms.ValidationError("Leave for more than 4 days not allowed")
