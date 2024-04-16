from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from proiect.forms import ReviewerSignupForm,DocumentUploadForm
from proiect.models import UploadedDocument, ReviewerRequest
from django.contrib.auth import get_user_model
from sklearn.metrics.pairwise import cosine_similarity
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth import get_user_model

import spacy
import numpy as np
import requests

def index(request):

    country = get_country_from_ip(request)
    
    if country:
        country_reviewer_count = get_user_model().objects.filter(is_reviewer=True # , country=country
                                                                 ).count()
    else:
        country = "Your Location"
        country_reviewer_count = 0
    
    reviewer_count = get_user_model().objects.filter(is_reviewer=True).count()

    context = {
        "title": "Home",
        'country': country,
        'country_reviewer_count': country_reviewer_count,
        'reviewer_count': reviewer_count,
    }
    return render(request, "index.html", context)

nlp = spacy.load("en_core_web_md")

#ai-testing
@login_required
def perform_simple_test(request, document_id):

    user_document = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    
    reference_documents = UploadedDocument.objects.exclude(user=request.user).exclude(id=document_id)

    document_content_bytes = user_document.document.read()
    document_content = document_content_bytes.decode('utf-8') if isinstance(document_content_bytes, bytes) else document_content_bytes

    query_embedding = nlp(document_content).vector.reshape(1, -1)

    reference_embeddings = [nlp(doc.document.read().decode('utf-8')).vector for doc in reference_documents]
    reference_embeddings = np.array(reference_embeddings).reshape(len(reference_embeddings), -1)

    similarity_threshold = 0.98

    similarity_values = cosine_similarity(query_embedding, reference_embeddings)[0]
    max_similarity = max(similarity_values)

    print("Query Vector:", query_embedding)
    print("Reference Vectors:", reference_embeddings)
    print("Cosine Similarity Values:", similarity_values)

    if max_similarity < similarity_threshold:
        test_result = "Test passed"
    else:
        test_result = "Test failed"

    return render(request, 'simple_test_result.html', {'user_document': user_document, 'test_result': test_result})



#user
@login_required
def user_dash(request):
    documents = UploadedDocument.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_document = form.save(commit=False)
            new_document.user = request.user
            new_document.save()
            return redirect('user_dash')
    else:
        form = DocumentUploadForm()

    return render(request, 'user_dashboard.html', {'form': form, 'documents': documents})

@login_required
def remove_document(request, document_id):
    document = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    document.delete()
    return redirect('user_dash')

@login_required
def send_to_review(request, document_id):
    document = get_object_or_404(UploadedDocument, id=document_id, user=request.user)

    if request.method == 'POST':
        workplace = request.POST.get('workplace')
        topic = request.POST.get('topic')

        reviewers = get_user_model().objects.filter(is_reviewer=True).exclude(current_workplace=workplace)

        for reviewer in reviewers:
            UploadedDocument.objects.create(
                user=reviewer,
                document=document.document,
                workplace=workplace,
                topic=topic
            )

        return redirect('user_dash')

    return render(request, 'user_dashboard.html', {'document': document, 'form': DocumentUploadForm()})

#reviewer
@login_required
def reviewer_dash(request):
    reviewer = request.user

    documents_to_review = UploadedDocument.objects.filter(user=reviewer)

    return render(request, "reviewer_dashboard.html", {'documents_to_review': documents_to_review})

#admin
@login_required
def admin_dash(request):
    signup_requests = ReviewerRequest.objects.all()
    print(signup_requests)
    return render(request, "admin_dashboard.html", {'signup_requests': signup_requests})

def approve_signup_request(request, request_id):
    signup_request = get_object_or_404(ReviewerRequest, id=request_id)
    
    user = get_user_model().objects.create_user(
        username=signup_request.username,
        email=signup_request.email,
        password=signup_request.password,
        is_active=True,
        is_reviewer=True
    )

    signup_request.delete()

    return redirect('admin_dash')

def deny_signup_request(request, request_id):
    signup_request = get_object_or_404(ReviewerRequest, id=request_id)
    signup_request.delete()
    return redirect('admin_dash')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def signup_user(request):
    if request.method == 'POST':
        form = ReviewerSignupForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ReviewerSignupForm(initial={'is_reviewer': False})

    form.fields['is_reviewer'].disabled = True

    return render(request, 'signup_user.html', {'form': form})

def signup_reviewer(request):
    if request.method == 'POST':
        form = ReviewerSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']


            ReviewerRequest.objects.create(
                email=email,
                username=username,
                current_workplace=form.cleaned_data['current_workplace'],
                references=form.cleaned_data['references'],
                password=password
            )

            return redirect('signup_reviewer_confirmation')
    else:
        form = ReviewerSignupForm()

    return render(request, 'signup_reviewer.html', {'form': form})

def signup_reviewer_confirmation(request):

    return render(request, "signup_reviewer_confirmation.html")

def your_view(request):
    user = request.user

    return render(request, 'base.html', {'user': user})


#help

def help_page(request):
    return render(request, 'help.html')

def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('title')
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_mail(
            'Contact Form Submission',
            f'Title: {name}\nEmail: {email}\nMessage: {message}',
            email,
            ['mihaixz4@gmail.com'],
            fail_silently=False,
        )

        return JsonResponse({'status': 'success'})
    
#ip geo


def get_country_from_ip(request):
    
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        country = data['country']
        return country
    except Exception as e:
        return None
    

