from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import UploadedDocument
from .models import Conference

class ReviewerSignupForm(UserCreationForm):

    email = forms.EmailField(max_length=254, required=True)
    current_workplace = forms.CharField(max_length=255, required=True)
    references = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'current_workplace', 'references']

    is_reviewer = forms.BooleanField(label='Become a Reviewer', required=False)


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ['document', 'workplace', 'topic']


class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name', 'start_date', 'end_date', 'location', 'description', 'picture']