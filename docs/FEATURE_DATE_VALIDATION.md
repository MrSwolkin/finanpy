# Transaction Date Validation Feature

## Overview
This feature implements smart date validation for transaction forms, allowing future dates for scheduled transactions while warning users about potential typos or very distant dates.

## Business Requirements

### Supported Use Cases
- **Scheduled bill payments**: Users can enter future bill payment dates
- **Expected salary deposits**: Users can record expected salary on a specific future date
- **Planned expenses**: Users can plan future purchases or expenses
- **Historical transactions**: Users can record past transactions up to 10 years ago

### Validation Rules

#### 1. Future Dates (Allowed with Warnings)
**Regular Warning (0-365 days in future)**
- Shows friendly message with time context
- Examples:
  - Tomorrow: "Nota: Esta transação está agendada para o futuro (amanhã)."
  - 7 days: "Nota: Esta transação está agendada para o futuro (em 7 dias)."
  - 3 months: "Nota: Esta transação está agendada para o futuro (em aproximadamente 3 meses)."

**Strong Warning (>365 days in future)**
- Shows stronger warning to catch potential typos
- Example: "Atenção: Esta data está 2.0 anos no futuro. Verifique se a data está correta."
- User can still save the transaction

#### 2. Past Dates
**Valid (0-10 years ago)**
- No warnings shown
- Allows recording historical transactions

**Invalid (>10 years ago)**
- Validation error (prevents save)
- Error message: "A data da transação não pode ser anterior a 10 anos atrás. Verifique se a data está correta."

## Technical Implementation

### 1. Form Validation (`transactions/forms.py`)

```python
def clean_transaction_date(self):
    """
    Custom validation for transaction_date field.
    - Allows future dates with warnings
    - Shows stronger warning for dates >1 year in future
    - Validates dates are not >10 years in the past
    """
    transaction_date = self.cleaned_data.get('transaction_date')

    if transaction_date is None:
        return transaction_date

    today = date.today()

    # Check if date is too far in the past
    ten_years_ago = today - timedelta(days=365 * 10)
    if transaction_date < ten_years_ago:
        raise forms.ValidationError(...)

    # Check if date is in the future
    if transaction_date > today:
        days_in_future = (transaction_date - today).days

        if days_in_future > 365:
            # Strong warning
            self.warnings['transaction_date'] = ...
        else:
            # Regular warning
            self.warnings['transaction_date'] = ...

    return transaction_date
```

### 2. Warning System

**Custom Attribute**
- Warnings stored in `self.warnings` dictionary
- Initialized in `__init__()` method
- Does not prevent form validation

**Key Difference from Errors**
- Errors (`form.errors`): Block form submission
- Warnings (`form.warnings`): Allow submission but inform user

### 3. Template Display (`templates/transactions/transaction_form.html`)

**Warning UI (Amber/Yellow)**
```html
{% if form.warnings.transaction_date %}
<div class="mt-2 bg-amber-500/10 border border-amber-500/30 rounded-lg p-3">
    <div class="flex items-start">
        <svg class="w-5 h-5 text-amber-400 mr-2 flex-shrink-0 mt-0.5">
            <!-- Warning triangle icon -->
        </svg>
        <p class="text-sm text-amber-300">{{ form.warnings.transaction_date }}</p>
    </div>
</div>
{% endif %}
```

**Error UI (Red)**
```html
{% if form.transaction_date.errors %}
<div id="id_transaction_date_error" role="alert" class="mt-2">
    {% for error in form.transaction_date.errors %}
    <p class="text-sm text-red-400">{{ error }}</p>
    {% endfor %}
</div>
{% endif %}
```

## Testing

### Test Coverage
All tests located in `transactions/tests.py`:

1. **test_today_date_no_warning**: Today's date has no warnings
2. **test_past_date_no_warning**: Past dates (within 10 years) have no warnings
3. **test_tomorrow_warning**: Tomorrow shows "amanhã" warning
4. **test_future_days_warning**: Future days show "em X dias" warning
5. **test_future_months_warning**: Future months show "aproximadamente X meses" warning
6. **test_future_one_year_regular_warning**: 1 year future shows regular warning
7. **test_future_two_years_strong_warning**: 2 years future shows strong "Atenção" warning
8. **test_ten_years_past_no_error**: Exactly 10 years ago is valid (edge case)
9. **test_eleven_years_past_error**: >10 years ago raises validation error
10. **test_warning_does_not_prevent_save**: Warnings don't block form submission

### Running Tests
```bash
python manage.py test transactions.tests.TransactionFormDateValidationTestCase
```

All 10 tests pass successfully.

## Design System

### Color Scheme
- **Warnings**: Amber/Yellow (`bg-amber-500/10`, `border-amber-500/30`, `text-amber-300`)
- **Errors**: Red (`text-red-400`)
- **Icons**: Warning triangle for alerts

### Accessibility
- `role="alert"` on warning and error containers
- SVG icons with proper sizing
- Clear color contrast (WCAG compliant)

## User Experience

### Workflow Examples

**Example 1: Recording Future Bill Payment**
1. User enters bill payment for next month (30 days)
2. Form shows amber warning: "Nota: Esta transação está agendada para o futuro (em 30 dias)."
3. User can still save the transaction
4. Transaction is recorded and counted in balance

**Example 2: Typo Detection**
1. User accidentally enters date 5 years in future
2. Form shows strong amber warning: "Atenção: Esta data está 5.0 anos no futuro..."
3. User realizes mistake and corrects the date
4. Prevents data entry errors

**Example 3: Historical Transaction**
1. User enters transaction from 2 years ago
2. No warnings shown
3. Transaction saved normally

**Example 4: Very Old Date (Error)**
1. User enters date from 2005 (21 years ago)
2. Form shows red error: "A data da transação não pode ser anterior a 10 anos atrás..."
3. Form cannot be submitted
4. User must correct the date

## Future Enhancements

Potential improvements for future sprints:

1. **User Preferences**: Allow users to configure warning thresholds
2. **Scheduled Transaction Flag**: Add a boolean field to explicitly mark scheduled transactions
3. **Recurring Transactions**: Support for recurring scheduled transactions
4. **Calendar Integration**: Visual calendar picker with warning indicators
5. **Transaction Status**: Add status field (pending/completed) for future transactions

## Files Modified

1. `/Users/erickswolkin/IA_MASTER/finanpy/transactions/forms.py`
   - Added `clean_transaction_date()` method
   - Initialized `self.warnings` dictionary in `__init__()`
   - Added imports: `date`, `timedelta`

2. `/Users/erickswolkin/IA_MASTER/finanpy/templates/transactions/transaction_form.html`
   - Added warning display block after date field
   - Amber-colored warning UI with triangle icon

3. `/Users/erickswolkin/IA_MASTER/finanpy/transactions/tests.py`
   - Created comprehensive test suite with 10 test cases
   - Tests all validation scenarios

## Commit Message
```
feat: add smart date validation for transactions

Implement warning system for future transaction dates to support
scheduled payments and planned expenses while preventing typos.

Features:
- Allow future dates with contextual warnings (tomorrow, X days, X months)
- Strong warning for dates >1 year in future
- Validation error for dates >10 years in past
- Custom warning system (non-blocking)
- Amber-colored warning UI distinct from errors
- Comprehensive test coverage (10 tests)

Supports use cases:
- Scheduled bill payments
- Expected salary deposits
- Planned future expenses
- Historical transactions (up to 10 years)

All messages in Portuguese (pt-BR).

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```
