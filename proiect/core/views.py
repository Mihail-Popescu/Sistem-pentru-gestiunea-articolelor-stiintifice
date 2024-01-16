from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from proiect.forms import ReviewerSignupForm,DocumentUploadForm
from proiect.models import UploadedDocument, ReviewerRequest
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

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
        return redirect('user_dash')

    return render(request, 'user_dashboard.html', {'document': document, 'form': DocumentUploadForm()})

#reviewer
@login_required
def reviewer_dash(request):

    return render(request, "reviewer_dashboard.html")

#admin
@login_required
def admin_dash(request):
    signup_requests = ReviewerRequest.objects.all()
    print(signup_requests)
    return render(request, "admin_dashboard.html", {'signup_requests': signup_requests})

def approve_signup_request(request, request_id):
    signup_request = get_object_or_404(ReviewerRequest, id=request_id)
    
    # Create a new user with the provided information
    user = get_user_model().objects.create_user(
        username=signup_request.username,
        email=signup_request.email,
        password=signup_request.password,  # Use the hashed password
        is_active=True,
        is_reviewer=True
    )

    # After processing, you can delete the reviewer request
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
            password = form.cleaned_data['password1']  # Change here


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