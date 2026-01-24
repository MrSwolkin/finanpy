# Enhanced Messages System - Finanpy

## Overview

The enhanced messages system provides a modern, accessible notification experience with smooth animations, auto-dismiss functionality, and progress indicators.

## Features

1. **Auto-dismiss messages** - Messages automatically disappear after 5 seconds (except errors)
2. **Smooth animations** - Slide-in from right, fade-out on dismiss
3. **Progress bar** - Visual indicator showing remaining time
4. **Pause on hover** - Timer pauses when hovering over message
5. **Stack management** - Multiple messages display in a vertical stack
6. **Accessibility** - ARIA live regions for screen readers
7. **Responsive** - Works on mobile, tablet, and desktop

## File Locations

- **JavaScript**: `/static/js/messages.js`
- **Template Partial**: `/templates/partials/messages.html`
- **Base Template**: `/templates/base/base.html` (includes the script)

## Usage in Django Views

### Basic Usage

```python
from django.contrib import messages
from django.shortcuts import redirect

def my_view(request):
    # Success message (auto-dismisses after 5 seconds)
    messages.success(request, 'Conta criada com sucesso!')

    # Error message (stays until manually closed)
    messages.error(request, 'Erro ao processar sua solicitação.')

    # Warning message (auto-dismisses after 5 seconds)
    messages.warning(request, 'Atenção: Esta ação não pode ser desfeita.')

    # Info message (auto-dismisses after 5 seconds)
    messages.info(request, 'Seus dados foram atualizados.')

    return redirect('some_url')
```

### Message Types and Behavior

| Type      | Auto-dismiss | Duration | Color  |
|-----------|--------------|----------|--------|
| `success` | Yes          | 5s       | Green  |
| `error`   | No           | Manual   | Red    |
| `warning` | Yes          | 5s       | Yellow |
| `info`    | Yes          | 5s       | Blue   |

## JavaScript API

The messages system exposes a global API for programmatic message creation.

### Adding Messages via JavaScript

```javascript
// Add success message
window.FinanpyMessages.addMessage('Operação realizada com sucesso!', 'success');

// Add error message
window.FinanpyMessages.addMessage('Erro ao processar dados.', 'error');

// Add warning message
window.FinanpyMessages.addMessage('Atenção necessária.', 'warning');

// Add info message
window.FinanpyMessages.addMessage('Informação importante.', 'info');
```

### Dismiss All Messages

```javascript
// Dismiss all currently visible messages
window.FinanpyMessages.dismissAll();
```

## Template Integration

The messages partial is automatically included in `base.html`:

```django
{% include "partials/messages.html" %}
```

Messages are rendered in the template and automatically enhanced with JavaScript.

## Animations

### Slide-in Animation
- **Direction**: From right
- **Duration**: 300ms
- **Easing**: ease-out

### Fade-out Animation
- **Direction**: To right
- **Duration**: 300ms
- **Easing**: ease-in

### Progress Bar
- **Duration**: 5 seconds (for auto-dismissing messages)
- **Behavior**: Shrinks from 100% to 0%
- **Pause**: On hover

## Hover Behavior

When hovering over a message:
1. Timer pauses
2. Message slightly scales up (1.02x)
3. Shadow increases
4. Progress bar stops animating

When mouse leaves:
1. Timer resumes with remaining time
2. Message returns to normal scale
3. Progress bar continues

## Accessibility Features

1. **ARIA Live Regions**: Messages announced to screen readers
2. **Role="alert"**: Proper semantic HTML
3. **Keyboard Support**: Focus management for close buttons
4. **Screen Reader Text**: "sr-only" labels for icons and actions

## Styling

### Color Scheme (Dark Mode)

Messages follow the Finanpy design system:

```css
/* Success */
bg-green-500/10 text-green-400 border-green-500/30
progress: bg-green-500

/* Error */
bg-red-500/10 text-red-400 border-red-500/30
progress: bg-red-500

/* Warning */
bg-yellow-500/10 text-yellow-400 border-yellow-500/30
progress: bg-yellow-500

/* Info */
bg-blue-500/10 text-blue-400 border-blue-500/30
progress: bg-blue-500
```

### Positioning

- **Position**: Fixed top-right
- **Z-index**: 9999 (above all other elements)
- **Spacing**: 3 (0.75rem) between messages
- **Max Width**: sm (24rem)

## Example Implementation

### In a Class-Based View

```python
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy

class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('accounts:account_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(
            self.request,
            f'Conta "{form.instance.name}" criada com sucesso!'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Erro ao criar conta. Verifique os campos e tente novamente.'
        )
        return super().form_invalid(form)
```

### In a Function-Based View

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        transaction_description = transaction.description
        transaction.delete()

        messages.success(
            request,
            f'Transação "{transaction_description}" excluída com sucesso!'
        )
        return redirect('transactions:transaction_list')

    return render(request, 'transactions/transaction_confirm_delete.html', {
        'transaction': transaction
    })
```

## Advanced Usage

### Dynamic Messages with AJAX

```javascript
// After successful AJAX request
fetch('/api/endpoint/', {
    method: 'POST',
    // ... request config
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        window.FinanpyMessages.addMessage(
            'Dados salvos com sucesso!',
            'success'
        );
    } else {
        window.FinanpyMessages.addMessage(
            'Erro ao salvar dados.',
            'error'
        );
    }
});
```

### Integration with Forms

```javascript
// After form validation
const form = document.querySelector('#my-form');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Validate form...
    if (!isValid) {
        window.FinanpyMessages.addMessage(
            'Preencha todos os campos obrigatórios.',
            'warning'
        );
        return;
    }

    // Submit form...
});
```

## Browser Support

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile browsers: Full support

## Performance

- Minimal DOM manipulation
- Uses `requestAnimationFrame` for smooth animations
- MutationObserver for efficient dynamic message detection
- Automatic cleanup of removed messages

## Troubleshooting

### Messages not appearing

1. Ensure `{% include "partials/messages.html" %}` is in your template
2. Check that `messages.js` is loaded in base.html
3. Verify browser console for JavaScript errors

### Messages not auto-dismissing

1. Check message type (errors don't auto-dismiss)
2. Verify `data-message-type` attribute is set correctly
3. Ensure JavaScript is enabled

### Progress bar not animating

1. Check that `data-message-progress` element exists
2. Verify message type is not 'error'
3. Check browser console for errors

## Future Enhancements

Potential improvements for future versions:

- [ ] Sound notifications (optional)
- [ ] Custom durations per message
- [ ] Grouped messages (collapse similar messages)
- [ ] Position options (top-left, bottom-right, etc.)
- [ ] Swipe to dismiss on mobile
- [ ] Message history/log
- [ ] Rich content support (HTML formatting)

## References

- Django Messages Framework: https://docs.djangoproject.com/en/5.1/ref/contrib/messages/
- ARIA Live Regions: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Live_Regions
- Web Animations API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API
