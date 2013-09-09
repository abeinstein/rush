from django import forms
from .models import Rush

class RushCreateForm(forms.ModelForm):
    class Meta:
        model = Rush
        fields = ['first_name', 'last_name', 'phone_number', 
                'email', 'dorm', 'hometown', 'picture']