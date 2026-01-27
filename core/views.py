"""
Core views for the Finanpy application.

This module contains the main dashboard view that displays financial overview,
balance information, recent transactions, and category summaries with period filtering.
"""
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q, Case, When, DecimalField, Value
from django.views.generic import TemplateView

from accounts.models import Account
from transactions.models import Transaction
from categories.models import Category


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard view displaying financial overview for the logged-in user.
    Includes total balance, period income/expenses, recent transactions,
    and category summary with period filtering.
    """
    template_name = 'dashboard/dashboard.html'

    def get_period_dates(self):
        """
        Calculate date range based on the selected period parameter.
        Returns tuple (date_from, date_to).
        """
        period = self.request.GET.get('period', 'current_month')
        today = date.today()

        if period == 'last_month':
            # First day of last month
            first_day_current = today.replace(day=1)
            last_month_last_day = first_day_current - timedelta(days=1)
            date_from = last_month_last_day.replace(day=1)
            date_to = last_month_last_day

        elif period == 'last_3_months':
            # 3 months ago from today
            date_to = today
            date_from = today - timedelta(days=90)

        elif period == 'current_year':
            # January 1st to today
            date_from = today.replace(month=1, day=1)
            date_to = today

        elif period == 'custom':
            # Custom date range from GET parameters
            date_from_str = self.request.GET.get('date_from')
            date_to_str = self.request.GET.get('date_to')

            try:
                date_from = date.fromisoformat(date_from_str) if date_from_str else today.replace(day=1)
                date_to = date.fromisoformat(date_to_str) if date_to_str else today
            except (ValueError, TypeError):
                # Fallback to current month if invalid dates
                date_from = today.replace(day=1)
                date_to = today
        else:
            # Default: current_month
            date_from = today.replace(day=1)
            date_to = today

        return date_from, date_to

    def get_total_balance(self):
        """
        Calculate total balance from all active accounts.
        """
        total = Account.objects.filter(
            user=self.request.user,
            is_active=True
        ).aggregate(
            total=Sum('current_balance')
        )['total']

        return total or Decimal('0.00')

    def get_period_totals(self, date_from, date_to):
        """
        Calculate total income and expenses for the specified period in a single query.
        Uses conditional aggregation to reduce database queries from 2 to 1.
        """
        totals = Transaction.objects.filter(
            user=self.request.user,
            transaction_date__gte=date_from,
            transaction_date__lte=date_to
        ).aggregate(
            income=Sum(
                Case(
                    When(transaction_type=Transaction.INCOME, then='amount'),
                    default=Value(0),
                    output_field=DecimalField()
                )
            ),
            expense=Sum(
                Case(
                    When(transaction_type=Transaction.EXPENSE, then='amount'),
                    default=Value(0),
                    output_field=DecimalField()
                )
            )
        )

        return {
            'income': totals['income'] or Decimal('0.00'),
            'expense': totals['expense'] or Decimal('0.00'),
        }

    def get_recent_transactions(self):
        """
        Get the 5 most recent transactions.
        """
        return Transaction.objects.filter(
            user=self.request.user
        ).select_related(
            'account', 'category'
        ).order_by(
            '-transaction_date', '-created_at'
        )[:5]

    def get_category_summary(self, date_from, date_to):
        """
        Get top 5 expense categories by total amount for the period.
        Returns list of dicts with category info and total.
        """
        category_totals = Transaction.objects.filter(
            user=self.request.user,
            transaction_type=Transaction.EXPENSE,
            transaction_date__gte=date_from,
            transaction_date__lte=date_to
        ).values(
            'category__id',
            'category__name',
            'category__color'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')[:5]

        return list(category_totals)

    def get_context_data(self, **kwargs):
        """
        Add dashboard data to template context.
        Optimized to reduce database queries using conditional aggregation.
        """
        context = super().get_context_data(**kwargs)

        # Get period dates
        date_from, date_to = self.get_period_dates()

        # Calculate metrics
        total_balance = self.get_total_balance()
        period_totals = self.get_period_totals(date_from, date_to)
        period_income = period_totals['income']
        period_expenses = period_totals['expense']
        period_balance = period_income - period_expenses

        # Get data
        recent_transactions = self.get_recent_transactions()
        category_summary = self.get_category_summary(date_from, date_to)

        # Add to context
        context.update({
            'total_balance': total_balance,
            'period_income': period_income,
            'period_expenses': period_expenses,
            'period_balance': period_balance,
            'recent_transactions': recent_transactions,
            'category_summary': category_summary,
            'selected_period': self.request.GET.get('period', 'current_month'),
            'date_from': date_from,
            'date_to': date_to,
        })

        return context
