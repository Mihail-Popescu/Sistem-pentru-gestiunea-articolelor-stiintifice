from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ReviewerSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'is_reviewer')

    is_reviewer = forms.BooleanField(label='Become a Reviewer', required=False)
