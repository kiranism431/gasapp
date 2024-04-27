from django.urls import path
from .views import submit_request_view, track_request, login_view, register_user

urlpatterns = [
    path('submit_request/', submit_request_view, name='submit_request'),
    path('track_request/', track_request, name='track_request'),
    path('login/', login_view, name='login'),
    path('register/', register_user, name='register'),
]
