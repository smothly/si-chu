from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', include('allauth.urls')),

    path('mypage/', views.my_page, name="account_mypage"),
    path('mypage/email', views.email_update, name="email_update"),
    path('mypage/profile', views.profile_update, name="profile_update"),

    path('favorite/', views.add_favorite_lecture, name='add_favorite_lecture'),
    path('email/action/', views.EmailView.as_view(), name="email_action"),
    path('email-complete', TemplateView.as_view(template_name="account/email_complete.html"), name="email_complete"),
]
