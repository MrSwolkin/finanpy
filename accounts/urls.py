from django.urls import path

from .views import (
    AccountListView,
    AccountCreateView,
    AccountDetailView,
    AccountUpdateView,
    AccountDeleteView,
)

app_name = 'accounts'

urlpatterns = [
    path('', AccountListView.as_view(), name='list'),
    path('create/', AccountCreateView.as_view(), name='create'),
    path('<int:pk>/', AccountDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', AccountUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', AccountDeleteView.as_view(), name='delete'),
]
