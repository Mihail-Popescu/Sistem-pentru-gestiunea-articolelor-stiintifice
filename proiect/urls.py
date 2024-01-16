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
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
