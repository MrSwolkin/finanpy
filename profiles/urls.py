from django.urls import path

from .views import ProfileDetailView, ProfileUpdateView

app_name = 'profiles'

urlpatterns = [
    path('profile/', ProfileDetailView.as_view(), name='detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit'),
]
