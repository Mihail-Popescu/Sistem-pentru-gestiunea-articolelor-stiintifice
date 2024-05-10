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
from docx import Document
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import redirect
from os.path import basename

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
    return render(request, "main_templates/index.html", context)

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

    return render(request, 'review_templates/simple_test_result.html', {'user_document': user_document, 'test_result': test_result})



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

    return render(request, 'dashboard_templates/user_dashboard.html', {'form': form, 'documents': documents})

@login_required
def remove_document(request, document_id):
    document = get_object_or_404(UploadedDocument, id=document_id, user=request.user)
    document.delete()
    # Redirect to the current page
    return redirect(request.META.get('HTTP_REFERER', ''))

@login_required
def send_to_review(request, document_id):
    document = get_object_or_404(UploadedDocument, id=document_id, user=request.user)

    if request.method == 'POST':
        workplace = request.POST.get('workplace')
        topic = request.POST.get('topic')

        # Update the status of the document to "SUBMITTED"
        document.status = 'SUBMITTED'
        document.save()

        reviewers = get_user_model().objects.filter(is_reviewer=True).exclude(current_workplace=workplace)

        for reviewer in reviewers:
            UploadedDocument.objects.create(
                user=reviewer,
                document=document.document,
                workplace=workplace,
                topic=topic,
                status='SUBMITTED',
                reviewer=reviewer
            )

        return redirect('user_dash')

    return render(request, 'user_dashboard.html', {'document': document, 'form': DocumentUploadForm()})


#reviewer
@login_required
def reviewer_dash(request):
    reviewer = request.user
    submitted_documents = UploadedDocument.objects.filter(user=reviewer, status='SUBMITTED')
    reviewing_documents = UploadedDocument.objects.filter(user=reviewer, status='UNDER_REVIEW')

    search_query = request.GET.get('search_query')
    search_workplace = request.GET.get('search_workplace')
    search_topic = request.GET.get('search_topic')

    if search_query:
        # Create a Q object to construct the query
        query_filter = Q()

        if search_workplace and search_topic:
            # Search in both workplace and topic
            query_filter |= Q(workplace__icontains=search_query) | Q(topic__icontains=search_query)
        elif search_workplace:
            # Search in workplace only
            query_filter |= Q(workplace__icontains=search_query)
        elif search_topic:
            # Search in topic only
            query_filter |= Q(topic__icontains=search_query)
        else:
            # No checkbox selected, search in both workplace and topic
            query_filter |= Q(workplace__icontains=search_query) | Q(topic__icontains=search_query)

        # Apply the filter to the queryset
        submitted_documents = submitted_documents.filter(query_filter)

        if not submitted_documents.exists():
            # If no document matches the query, set a message
            no_document_message = "No document matched the query."
        else:
            no_document_message = None
    else:
        search_query = None
        no_document_message = None

    return render(request, "dashboard_templates/reviewer_dashboard.html", {'submitted_documents': submitted_documents, 'reviewing_documents': reviewing_documents, 'search_query': search_query, 'no_document_message': no_document_message})

@login_required
def choose_document(request, document_id):
    # Get the document with the provided document_id
    document = get_object_or_404(UploadedDocument, id=document_id, user=request.user, status='SUBMITTED')
    document.status = 'UNDER_REVIEW'
    document.save()
    # Get the name of the current document
    document_name = basename(document.document.name)
    
    # Query all documents with the same name
    documents_with_same_name = UploadedDocument.objects.filter(document__icontains=document_name)
    
    # Loop through each document with the same name
    for document in documents_with_same_name:
        # Check if the reviewer field is NULL
        if not document.reviewer:
            # Update the status to 'UNDER_REVIEW'
            document.status = 'UNDER_REVIEW'
            document.save()
    
    # Redirect to the reviewer dashboard
    return redirect('reviewer_dash')

#admin
@login_required
def admin_dash(request):
    signup_requests = ReviewerRequest.objects.all()

    # Retrieve ongoing reviews
    ongoing_reviews = UploadedDocument.objects.filter(status='UNDER_REVIEW', reviewer=None)

    # Initialize a dictionary to hold ongoing reviewers for each document
    ongoing_reviewers_dict = {}

    # Handle search query
    search_query = request.GET.get('search_query')
    if search_query:
        ongoing_reviews = ongoing_reviews.filter(document__icontains=search_query)

    # Identify users and reviewers for each document
    for document in ongoing_reviews:
        # Fetch ongoing reviewers for the current document
        ongoing_reviewers = UploadedDocument.objects.filter(
            document__icontains=document.document.name,
            reviewer__isnull=False,
            status='UNDER_REVIEW'
        ).values_list('reviewer__username', 'reviewer__email').distinct()

        # Add ongoing reviewers to the dictionary
        ongoing_reviewers_dict[document] = ongoing_reviewers

    return render(request, "dashboard_templates/admin_dashboard.html", {
        'signup_requests': signup_requests,
        'ongoing_reviews': ongoing_reviews,
        'ongoing_reviewers_dict': ongoing_reviewers_dict,
        'search_query': search_query,  # Pass the search query back to the template
    })


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

    return render(request, 'auth_templates/login.html', {'form': form})

def signup_user(request):
    if request.method == 'POST':
        form = ReviewerSignupForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ReviewerSignupForm(initial={'is_reviewer': False})

    form.fields['is_reviewer'].disabled = True

    return render(request, 'auth_templates/signup_user.html', {'form': form})

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

    return render(request, 'auth_templates/signup_reviewer.html', {'form': form})

def signup_reviewer_confirmation(request):

    return render(request, "auth_templates/signup_reviewer_confirmation.html")

def your_view(request):
    user = request.user

    return render(request, 'main_templates/base.html', {'user': user})


#help

def help_page(request):
    return render(request, 'main_templates/help.html')

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
    

def preview_document(request, document_id):
    try:
        document = UploadedDocument.objects.get(id=document_id)
        file_path = document.document.path
        if file_path.endswith('.pdf'):
            # For PDF files, return the file directly
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
            return response
        elif file_path.endswith('.docx'):
            # For .docx files, extract text and return it
            doc = Document(file_path)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            return HttpResponse(text, content_type='text/plain; charset=utf-8')  # Set charset=utf-8
        else:
            # Handle other file types or unsupported types
            return HttpResponse("Unsupported file format")
    except UploadedDocument.DoesNotExist:
        return HttpResponse("Document not found", status=404)