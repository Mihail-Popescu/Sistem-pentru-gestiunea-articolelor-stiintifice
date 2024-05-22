from django.contrib.auth.models import AbstractUser
from django.db import models
from proiect.settings import AUTH_USER_MODEL

class CustomUser(AbstractUser): # diferentiem rolurile prin acestea:
    is_reviewer = models.BooleanField(default=False) #
    is_tracker = models.BooleanField(default=False) #
    is_organizer = models.BooleanField(default=False) #
    current_workplace = models.CharField(max_length=255, blank=True, null=True)
    references = models.TextField(blank=True, null=True)
    joined_conferences = models.ManyToManyField('Conference', blank=True, related_name='participants')

class Conference(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    picture = models.ImageField(upload_to='conference_pictures/', blank=True, null=True)
    organizer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_conferences')
    trackers = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='tracked_conferences')

class UploadedDocument(models.Model):
    STATUS_CHOICES = [
        ('UPLOADED', 'Uploaded'),
        ('SUBMITTED', 'Submitted for Review'),
        ('UNDER_REVIEW', 'Under Review'),
        ('REVIEWED', 'Reviewed'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.FileField(upload_to='uploaded_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    topic = models.CharField(max_length=255, default='', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UPLOADED')
    reviewer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reviewed_documents')
    conference = models.ForeignKey('Conference', on_delete=models.CASCADE, related_name='uploaded_documents', null=True, blank=True)
    feedback = models.ForeignKey('ReviewFeedback', on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback_documents')

class ReviewFeedback(models.Model):
    document = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    whats_wrong = models.TextField()
    what_can_be_improved = models.TextField()
    score = models.IntegerField()
    decision = models.CharField(max_length=50, choices=[
        ('reject', 'Reject'),
        ('accept_with_small_revisions', 'Accept with Small Revisions'),
        ('accept_with_major_revisions', 'Accept with Major Revisions'),
        ('accept', 'Accept'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

class ReviewerRequest(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    current_workplace = models.CharField(max_length=255)
    references = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"Signup Request for {self.username}"