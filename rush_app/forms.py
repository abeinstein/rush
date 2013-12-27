from django import forms
from .models import Rush, Frat

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class RushCreateForm(forms.ModelForm):
    class Meta:
        model = Rush
        fields = ['first_name', 'last_name', 'phone_number', 
                'email', 'dorm', 'hometown', 'picture']

class SignUpForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(required=True, widget=forms.PasswordInput)
    frat = forms.ModelChoiceField(required=True, queryset=Frat.objects.all(), 
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Select your fraternity/sorority")
    frat_password = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        frat_password = cleaned_data.get('frat_password')

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with that username already exists")

        if not check_password(frat_password, cleaned_data.get('frat').password):
            raise forms.ValidationError("Incorrect frat pasword.")

