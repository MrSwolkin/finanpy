# Form Validation System

## Overview

The Finanpy project implements a real-time form validation system that provides instant feedback to users as they fill out forms. The validation occurs on blur and input events, showing visual feedback with border colors and error messages in Portuguese.

## Implementation

### JavaScript Module

Location: `/static/js/validation.js`

The validation module is implemented as an IIFE (Immediately Invoked Function Expression) that exports a `FormValidator` class to `window.FinanpyValidation`.

### How It Works

1. **Initialization**: On DOM ready, the module finds all fields with `data-validate` attribute
2. **Event Listeners**: Attaches blur and input event listeners to each validated field
3. **Validation Rules**: Checks field value against data attributes (data-required, data-email, etc.)
4. **Visual Feedback**: Updates border colors and shows/hides error messages
5. **Accessibility**: Sets `aria-invalid` attribute for screen readers

## Validation Rules

### Available Data Attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| `data-validate` | Enable validation on this field | `data-validate="true"` |
| `data-required` | Field is required | `data-required="true"` |
| `data-email` | Must be valid email format | `data-email="true"` |
| `data-min-length` | Minimum character length | `data-min-length="8"` |
| `data-max-length` | Maximum character length | `data-max-length="100"` |
| `data-positive` | Must be positive number | `data-positive="true"` |
| `data-match` | Must match another field (by ID) | `data-match="id_password1"` |

### Error Messages (Portuguese)

- **Required**: "Este campo é obrigatório"
- **Email**: "Digite um email válido"
- **Min Length**: "Mínimo de {n} caracteres"
- **Max Length**: "Máximo de {n} caracteres"
- **Positive**: "Digite um valor positivo"
- **Match**: "Os campos não coincidem"

## Visual Feedback

### Field States

- **Neutral (untouched)**: `border-gray-600` (default gray border)
- **Valid**: `border-green-500` (green border)
- **Invalid**: `border-red-500` (red border + error message)

### Error Message Display

Error messages are inserted below the field with:
- Class: `validation-error mt-2 text-sm text-red-400`
- Role: `alert` (for accessibility)
- Shows first error only per field

## Usage Examples

### Signup Form

```html
<input
    type="email"
    name="email"
    id="id_email"
    class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg..."
    data-validate="true"
    data-required="true"
    data-email="true"
>

<input
    type="password"
    name="password1"
    id="id_password1"
    class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg..."
    data-validate="true"
    data-required="true"
    data-min-length="8"
>

<input
    type="password"
    name="password2"
    id="id_password2"
    class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg..."
    data-validate="true"
    data-required="true"
    data-match="id_password1"
>
```

### Transaction Form

```html
<input
    type="text"
    name="description"
    id="id_description"
    class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg..."
    data-validate="true"
    data-required="true"
>

<input
    type="number"
    name="amount"
    id="id_amount"
    class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg..."
    data-validate="true"
    data-required="true"
    data-positive="true"
>
```

## Django Form Integration

Add validation attributes to form widgets in `forms.py`:

```python
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': '...',
            'data-validate': 'true',
            'data-required': 'true',
            'data-email': 'true'
        })
    )

    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': '...',
            'data-validate': 'true',
            'data-required': 'true',
            'data-min-length': '8'
        })
    )
```

## Behavior

### Validation Triggers

1. **On Blur**: First validation happens when user leaves field
2. **On Input**: After first blur, validation updates on every keystroke
3. **On Change**: For select fields, validates on change event

### Important Notes

- **Client-side only**: Does NOT prevent form submission
- **Django handles server-side**: Always validate on backend
- **Progressive enhancement**: Forms work without JavaScript
- **Accessibility**: Uses aria-invalid for screen readers

## API

### Public Methods

```javascript
// Access the validator instance
const validator = window.FinanpyValidation;

// Validate all fields in a form
validator.validateForm(formElement);

// Validate a single field
validator.validateField(fieldElement);

// Reset validation state for a field
validator.resetField(fieldElement);

// Reset all fields in a form
validator.resetForm(formElement);
```

## Files Modified

### Core Files

1. **`/static/js/validation.js`** - Main validation module
2. **`/templates/base/base.html`** - Added script tag

### Form Files

1. **`/users/forms.py`** - Added validation attributes to signup form
2. **`/transactions/forms.py`** - Added validation to transaction form
3. **`/accounts/forms.py`** - Added validation to account form
4. **`/categories/forms.py`** - Added validation to category form

### Template Files

1. **`/templates/users/login.html`** - Added validation attributes
2. **`/templates/transactions/transaction_form.html`** - Added validation to amount field

## Testing

To test the validation system:

1. Navigate to signup page (`/users/signup/`)
2. Try to submit empty fields - should see "Este campo é obrigatório"
3. Type invalid email - should see "Digite um email válido"
4. Type short password - should see "Mínimo de 8 caracteres"
5. Type mismatched passwords - should see "Os campos não coincidem"

## Future Enhancements

Potential improvements:

1. Add more validation rules (URL, phone, CPF/CNPJ)
2. Custom error messages per field
3. Async validation (check email availability)
4. Form-level validation (cross-field rules)
5. Integration with Django form errors on page load
6. Debounced validation for better performance
7. Visual success indicators (checkmark icons)
