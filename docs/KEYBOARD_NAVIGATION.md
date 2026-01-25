# Keyboard Navigation Accessibility Guide

This document describes the keyboard navigation accessibility features implemented in Finanpy.

## Overview

Finanpy implements comprehensive keyboard navigation support to ensure the application is fully accessible to users who navigate using keyboard only, including screen reader users and those with motor disabilities.

## Implemented Features

### 1. Tooltip Keyboard Support

**File:** `/static/js/tooltip-accessibility.js`

All tooltips in the application support keyboard interaction:

- **Tab**: Navigate to tooltip trigger elements
- **Enter/Space**: Toggle tooltip visibility
- **Escape**: Close active tooltip
- **Arrow Keys**: Close tooltip when navigating away

**Features:**
- All tooltip triggers are automatically made focusable (`tabindex="0"`)
- Proper ARIA attributes are applied (`role="button"`, `aria-describedby`)
- Only one tooltip can be active at a time
- Tooltips close automatically when focus moves away

**Usage:**
```html
<!-- Tooltip triggers are automatically enhanced -->
<span data-tooltip="Help text here" class="tooltip-help-icon">
    <svg>...</svg>
</span>
```

### 2. Navigation Dropdown Keyboard Support

**File:** `/static/js/navbar.js`

The user dropdown menu in the navbar provides full keyboard navigation:

**From Menu Button:**
- **Enter/Space**: Open dropdown and focus first item
- **Arrow Down**: Open dropdown and focus first item

**Within Dropdown Menu:**
- **Arrow Down**: Move to next menu item (wraps to first)
- **Arrow Up**: Move to previous menu item (wraps to last)
- **Home**: Jump to first menu item
- **End**: Jump to last menu item
- **Escape**: Close menu and return focus to button
- **Tab**: Close menu when tabbing out
- **Enter**: Activate menu item

**Focus Management:**
- When dropdown opens, focus moves to first menu item
- When dropdown closes, focus returns to menu button
- Menu items have `tabindex="-1"` when menu is closed
- Menu items have `tabindex="0"` when menu is open

### 3. Focus Visible Styles

**Files:**
- `/templates/partials/navbar.html`
- `/templates/base/base.html` (global styles)

All interactive elements have visible focus indicators:

**Desktop Navigation Links:**
```css
focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-900
```

**Buttons:**
```css
focus:outline-none focus:ring-2 focus:ring-purple-600
```

**Dropdown Menu Items:**
```css
focus:outline-none focus:bg-gray-700 focus:text-white
```

**Skip Link:**
- A skip-to-content link is provided as the first focusable element
- It becomes visible when focused
- Allows keyboard users to bypass navigation

### 4. Tab Order

The application follows a logical tab order:

1. **Skip to Content Link** (first)
2. **Logo/Brand**
3. **Desktop Navigation Links**
   - Dashboard
   - Contas
   - Transações
   - Categorias
4. **User Menu Button**
5. **Main Content Area**
6. **Footer Links**

The tab order matches the visual layout and follows user expectations.

### 5. Form Field Accessibility

**File:** `/static/js/form-accessibility.js`

All form fields are enhanced with:
- `aria-describedby` linking to help text and error messages
- `aria-invalid` state for fields with errors
- `aria-required` for required fields
- Live validation feedback

## Testing Keyboard Navigation

### Basic Testing

1. **Tab Navigation:**
   - Press Tab repeatedly to navigate through all interactive elements
   - Verify focus indicator is clearly visible on each element
   - Ensure tab order is logical and matches visual layout

2. **Skip Link:**
   - Press Tab once from page load
   - Verify "Pular para o conteúdo principal" appears
   - Press Enter to skip to main content

3. **Navigation Menu:**
   - Tab to navigation links
   - Press Enter to navigate
   - Verify focus styles are visible

4. **User Dropdown:**
   - Tab to user menu button
   - Press Enter or Arrow Down to open
   - Use Arrow keys to navigate menu items
   - Press Escape to close and verify focus returns to button

5. **Tooltips:**
   - Tab to a help icon (?)
   - Press Enter or Space to show tooltip
   - Press Escape to close
   - Tab away to close tooltip

### Screen Reader Testing

Test with NVDA (Windows), JAWS (Windows), or VoiceOver (macOS):

1. Verify all interactive elements are announced
2. Verify ARIA labels are read correctly
3. Verify form errors are announced
4. Verify dropdown menu state (expanded/collapsed) is announced

## Browser Compatibility

Keyboard navigation works in all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## WCAG Compliance

These implementations help meet the following WCAG 2.1 Level AA criteria:

- **2.1.1 Keyboard (Level A)**: All functionality is available via keyboard
- **2.1.2 No Keyboard Trap (Level A)**: Keyboard focus can be moved away from all components
- **2.4.3 Focus Order (Level A)**: Focus order is logical and preserves meaning
- **2.4.7 Focus Visible (Level AA)**: Keyboard focus indicator is visible
- **3.2.1 On Focus (Level A)**: Components don't initiate change of context on focus
- **4.1.2 Name, Role, Value (Level A)**: ARIA attributes properly convey state

## Future Improvements

Potential enhancements for future versions:

1. **Keyboard Shortcuts:**
   - Add global keyboard shortcuts (e.g., Alt+D for Dashboard)
   - Implement command palette (Ctrl+K)

2. **Enhanced Focus Management:**
   - Focus trapping in modals
   - Focus restoration after delete operations

3. **Roving Tabindex:**
   - Implement for table rows
   - Implement for card grids

4. **Search Autocomplete:**
   - Add keyboard navigation for search results
   - Arrow keys to navigate suggestions

## Troubleshooting

### Focus Indicator Not Visible

If focus indicators are not visible:
1. Check browser zoom level (should be 100% or higher)
2. Verify no custom CSS is overriding focus styles
3. Check browser settings for high contrast mode

### Dropdown Not Opening with Keyboard

If dropdown doesn't open:
1. Verify navbar.js is loaded (check browser console)
2. Check for JavaScript errors
3. Verify button has proper ARIA attributes

### Tooltips Not Responding to Keyboard

If tooltips don't respond:
1. Verify tooltips.js and tooltip-accessibility.js are loaded
2. Check that element has `data-tooltip` attribute
3. Verify no JavaScript errors in console

## Developer Guidelines

When adding new interactive elements:

1. **Always add focus styles:**
   ```html
   class="... focus:outline-none focus:ring-2 focus:ring-purple-500"
   ```

2. **Use semantic HTML:**
   - Use `<button>` for buttons
   - Use `<a>` for links
   - Use proper form elements

3. **Add ARIA attributes when needed:**
   - `aria-label` for icon-only buttons
   - `aria-expanded` for toggles
   - `aria-describedby` for additional context

4. **Test with keyboard:**
   - Tab through all interactive elements
   - Verify logical order
   - Test all keyboard interactions

5. **Test with screen reader:**
   - Verify announcements make sense
   - Check dynamic content updates are announced

## Resources

- [WebAIM: Keyboard Accessibility](https://webaim.org/techniques/keyboard/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN: Keyboard-navigable JavaScript widgets](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Keyboard-navigable_JavaScript_widgets)
