from django import forms
from .models import Rush, Frat
from .colleges import ALL_COLLEGES
from .greeks import ALL_GREEK_ORGS

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class RushCreateForm(forms.ModelForm):
    class Meta:
        model = Rush
        fields = ['first_name', 'last_name', 'phone_number', 
                'email', 'dorm', 'hometown', 'picture']

class SignUpForm(forms.Form):
    new_frat_created = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "hidden"}), required=False)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(required=True, widget=forms.PasswordInput)
    school = forms.ChoiceField(required=True, widget=forms.Select(attrs={"class": "form-control hidden"}),
        choices=[('', 'Select your school')] + ALL_COLLEGES)
    frat = forms.ChoiceField(required=True, widget=forms.Select(attrs={"class": "form-control hidden"}),
        choices=[('', 'Select your fraternity or sorority')] + ALL_GREEK_ORGS
        )
    frat_password = forms.CharField(required=True, widget=forms.PasswordInput)
    frat_password_confirmation = forms.CharField(required=False, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        school = cleaned_data.get('school')
        frat = cleaned_data.get('frat')
        frat_password = cleaned_data.get('frat_password')
        frat_password_confirmation = cleaned_data.get('frat_password_confirmation')
        new_frat_created = cleaned_data.get('new_frat_created')

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with that username already exists")

        # Error checking for joining an existing frat
        if not new_frat_created:
            try:
                frat_object = Frat.objects.get(name=frat, university=school)
            except Frat.DoesNotExist:
                raise forms.ValidationError("Fraternity does not exist")

            if not check_password(frat_password, frat_object.password):
                raise forms.ValidationError("Incorrect frat pasword.")

        # Error checking for creating a new frat
        else:
            if frat_password != frat_password_confirmation:
                raise forms.ValidationError("Fraternity passwords do not match")

            if Frat.objects.filter(name=frat, university=school).exists():
                raise forms.ValidationError("Fraternity already exists.")

        return cleaned_data
            

