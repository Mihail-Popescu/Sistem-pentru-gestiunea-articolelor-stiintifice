from django.contrib.auth.models import AbstractUser
from django.db import models
from proiect.settings import AUTH_USER_MODEL

class CustomUser(AbstractUser): # user normal si revieweri, ii diferentiem prin \/
    is_reviewer = models.BooleanField(default=False) #
    current_workplace = models.CharField(max_length=255, blank=True, null=True)
    references = models.TextField(blank=True, null=True)

class UploadedDocument(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.FileField(upload_to='uploaded_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    workplace = models.CharField(max_length=255, blank=True, null=True)
    topic = models.CharField(max_length=255, default='', blank=True)


class ReviewerRequest(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    current_workplace = models.CharField(max_length=255)
    references = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"Signup Request for {self.username}"