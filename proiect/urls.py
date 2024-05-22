"""hello_world URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from proiect.core import views as core_views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", core_views.index),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('help/', core_views.help_page, name='help'),
    path('login/', core_views.login_view, name='login'),
    path('signup/', core_views.signup_user, name='signup'),
    path('signup_reviewer/', core_views.signup_reviewer, name='signup_reviewer'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user_dash/', core_views.user_dash, name='user_dash'),
    path('reviewer_dash/', core_views.reviewer_dash, name='reviewer_dash'),
    path('admin_dash/', core_views.admin_dash, name='admin_dash'),
    path('user/remove_document/<int:document_id>/', core_views.remove_document, name='remove_document'),
    path('user/send_to_review/<int:document_id>/', core_views.send_to_review, name='send_to_review'),
    path('user/approve_signup_request/<int:request_id>/', core_views.approve_signup_request, name='approve_signup_request'),
    path('user/deny_signup_request/<int:request_id>/', core_views.deny_signup_request, name='deny_signup_request'),
    path('signup_reviewer_confirmation/', core_views.signup_reviewer_confirmation, name='signup_reviewer_confirmation'),
    path('contact_form/', core_views.contact_form, name='contact_form'),
    path('preview_document/<int:document_id>/', core_views.preview_document, name='preview_document'),
    path('choose_document/<int:document_id>/', core_views.choose_document, name='choose_document'),
    path('return_document/<int:document_id>/', core_views.return_document, name='return_document'),
    path('spell_check/', core_views.spell_check_view, name='spell_check'),
    path('ner_extraction/', core_views.ner_view, name='ner_extraction'),
    path('analyze_sentiment/', core_views.analyze_sentiment_view, name='analyze_sentiment'),
    path('compare_documents/', core_views.compare_documents_view, name='compare_documents'),
    path('change_user_roles/', core_views.change_user_roles, name='change_user_roles'),
    path('tracker_dash/', core_views.tracker_dash, name='tracker_dash'),
    path('organizer_dash/', core_views.organizer_dash, name='organizer_dash'),
    path('create_conference/', core_views.create_conference, name='create_conference'),
    path('delete_conference/<int:conference_id>/', core_views.delete_conference, name='delete_conference'),
    path('conferences/', core_views.conferences, name='conferences'),
    path('assign_user_to_conference/', core_views.assign_user_to_conference, name='assign_user_to_conference'),
    path('reject_document/<int:document_id>/', core_views.reject_document, name='reject_document'),
    path('match_reviewer/<int:document_id>/', core_views.match_reviewer, name='match_reviewer'),
    path('get_feedback/<int:document_id>/', core_views.get_feedback, name='get_feedback'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
