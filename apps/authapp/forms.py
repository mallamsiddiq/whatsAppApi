import django
from django import forms
from django.contrib.auth.forms import UserCreationForm

User = django.contrib.auth.get_user_model()

class SigupForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True, 
        help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['email', 'password1']