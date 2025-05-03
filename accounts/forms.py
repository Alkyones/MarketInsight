# forms.py
from django import forms
from django.contrib.auth.models import User

class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=255, required=True, label='')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='')
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.add_error(None, 'Invalid username or password.')
                return cleaned_data

            if not user.check_password(password):
                self.add_error(None, 'Invalid username or password.')
                return cleaned_data