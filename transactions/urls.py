from django.urls import path

from .views import (
    TransactionListView,
    TransactionCreateView,
    TransactionDetailView,
    TransactionUpdateView,
    TransactionDeleteView,
)

app_name = 'transactions'

urlpatterns = [
    path('', TransactionListView.as_view(), name='list'),
    path('create/', TransactionCreateView.as_view(), name='create'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', TransactionUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TransactionDeleteView.as_view(), name='delete'),
]
