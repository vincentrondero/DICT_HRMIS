from django import forms
from django.contrib.auth.hashers import make_password, check_password
from datetime import date
from Authentication.models import User
from .models import CleansedData

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'role', 'salary_grade']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = True
        self.fields['password'].help_text = 'Enter a strong password.'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)

        # Ensure the password is hashed before saving
        user.password = make_password(self.cleaned_data['password'])

        user.archived = False

        if commit:
            user.save()

        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'role', 'salary_grade']
        exclude = ['password']

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)

        if commit:
            user.save()

        return user
