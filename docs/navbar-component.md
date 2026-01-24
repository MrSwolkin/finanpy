# Navbar Component Documentation

## Overview

The Finanpy navbar is a fully responsive navigation component that provides consistent navigation across all authenticated pages of the application. It follows the project's Design System with dark mode theme and purple/blue gradients.

## Features

### Task 39.1 - Component Structure
- Located at: `templates/partials/navbar.html`
- Included in base template via `{% include 'partials/navbar.html' %}`
- Only renders for authenticated users (`{% if user.is_authenticated %}`)

### Task 39.2 - Logo/Brand
- **Brand Name**: "Finanpy" with gradient effect
- **Gradient**: `from-purple-600 to-blue-600`
- **Link**: Dashboard (`{% url 'dashboard' %}`)
- **Hover Effect**: Lighter gradient on hover

### Task 39.3 - Desktop Menu
- **Breakpoint**: Hidden below `lg` (1024px), visible on desktop
- **Navigation Links**:
  - Dashboard
  - Contas (Accounts)
  - Transações (Transactions)
  - Categorias (Categories)
- **Active State**: Highlighted with gradient background using `request.resolver_match.app_name`
- **Hover State**: Gray background on hover for inactive links

### Task 39.4 - Mobile Menu
- **Breakpoint**: Visible below `lg` (1024px)
- **Toggle Button**: Hamburger icon that transforms to close icon
- **Sidebar**: Drops down from navbar with full navigation
- **Features**:
  - User info section with avatar and email
  - All navigation links with icons
  - Profile and logout links at bottom
  - Active state highlighting same as desktop

### Task 39.5 - User Dropdown (Desktop)
- **Trigger**: Click on user button with avatar and name
- **Content**:
  - User email display
  - "Meu Perfil" link with icon
  - "Sair" (Logout) link with icon in red
- **Avatar Logic**:
  - Shows user's profile avatar if available
  - Falls back to gradient circle with first letter of name
  - Falls back to first letter of email if no profile
- **Animation**: Dropdown icon rotates 180° when open

### Task 39.6 - JavaScript Functionality
- **File**: `static/js/navbar.js`
- **Module Pattern**: IIFE for encapsulation
- **Features**:
  - Mobile menu toggle
  - User dropdown toggle
  - Click outside to close both menus
  - Escape key to close menus
  - Body scroll lock when mobile menu is open
  - Icon animations for hamburger/close

### Task 39.7 - Sticky Navbar
- **Position**: `sticky top-0`
- **Z-index**: `z-50` (above most content)
- **Background**: `bg-gray-900/95 backdrop-blur-md`
- **Scroll Effect**: Shadow (`shadow-xl`) added when scrolling past 10px
- **Performance**: Uses `requestAnimationFrame` for smooth scroll handling

## Technical Implementation

### Template Structure

```django
{% load static %}

{% if user.is_authenticated %}
<nav id="navbar" class="sticky top-0 z-50...">
    <div class="container mx-auto px-4 py-4 max-w-7xl">
        <!-- Logo -->
        <!-- Desktop Menu -->
        <!-- User Dropdown -->
        <!-- Mobile Button -->
    </div>
    <!-- Mobile Menu -->
</nav>
<script src="{% static 'js/navbar.js' %}"></script>
{% endif %}
```

### JavaScript Class

```javascript
class Navbar {
    constructor() {
        // Elements
        // State
        // Initialize
    }

    // Mobile menu methods
    toggleMobileMenu()
    openMobileMenu()
    closeMobileMenu()

    // User dropdown methods
    toggleUserDropdown()
    openUserDropdown()
    closeUserDropdown()

    // Event handlers
    initMobileMenu()
    initUserDropdown()
    initStickyNavbar()
    initClickOutside()
    initEscapeKey()
}
```

## Design System Compliance

### Colors
- **Background**: `bg-gray-900/95` with `backdrop-blur-md`
- **Border**: `border-gray-700`
- **Text**: `text-gray-100` (primary), `text-gray-300` (secondary), `text-gray-400` (tertiary)
- **Active State**: `bg-gradient-to-r from-purple-600 to-blue-600 text-white`
- **Hover State**: `hover:bg-gray-800` for inactive links

### Typography
- **Logo**: `text-2xl font-bold`
- **Nav Links**: `font-medium`
- **User Name**: `font-medium`
- **Dropdown Items**: `text-sm`

### Spacing
- **Container**: `px-4 py-4` with `max-w-7xl`
- **Desktop Links**: `space-x-1` between items, `px-4 py-2` per item
- **Mobile Links**: `space-y-1` between items

### Transitions
- All transitions use `duration-200`
- Smooth color and background changes
- Icon rotation animation for dropdowns

## URL Structure

The navbar uses Django's named URL patterns:

- Dashboard: `{% url 'dashboard' %}`
- Accounts: `{% url 'accounts:list' %}`
- Transactions: `{% url 'transactions:list' %}`
- Categories: `{% url 'categories:list' %}`
- Profile: `{% url 'profiles:detail' %}`
- Logout: `{% url 'users:logout' %}`

## Active State Detection

Uses Django's `request.resolver_match` to detect active page:

```django
{% with request.resolver_match.url_name as current_url %}
    <!-- For dashboard -->
    {% if current_url == 'dashboard' %}...{% endif %}

    <!-- For app sections -->
    {% if request.resolver_match.app_name == 'accounts' %}...{% endif %}
{% endwith %}
```

## Profile Integration

The navbar safely handles users without profiles:

```django
{% if user.profile and user.profile.avatar %}
    <img src="{{ user.profile.avatar.url }}">
{% else %}
    <div>{{ user.email|slice:":1"|upper }}</div>
{% endif %}
```

## Responsive Breakpoints

- **Mobile**: `< 1024px` - Mobile menu visible, desktop menu hidden
- **Desktop**: `≥ 1024px` (lg) - Desktop menu visible, mobile menu hidden

## Accessibility

- **ARIA Labels**: Menu buttons include `aria-label`, `aria-expanded`, `aria-haspopup`
- **Keyboard Support**: Escape key closes open menus
- **Focus States**: Visible focus rings on interactive elements
- **Screen Reader Text**: "Menu" label for mobile button

## Browser Compatibility

- Modern browsers with ES6 support
- CSS Grid and Flexbox
- Backdrop filter for blur effect
- CSS variables for gradient

## Performance Considerations

1. **JavaScript**: Minimal, efficient event handling
2. **Scroll Handler**: Throttled with `requestAnimationFrame`
3. **CSS Transitions**: Hardware-accelerated properties
4. **Mobile Menu**: Body scroll lock prevents double scrolling
5. **Click Outside**: Single document listener for all menus

## Future Enhancements

Potential improvements for future sprints:

1. Notification badge/icon
2. Search functionality
3. Theme switcher (light/dark mode)
4. Keyboard navigation for dropdown menus
5. Animation for mobile menu slide-in
6. Recent transactions dropdown
7. Quick actions menu

## Testing Checklist

- [ ] Logo links to dashboard
- [ ] Desktop menu shows all links
- [ ] Active page is highlighted
- [ ] Mobile menu toggles correctly
- [ ] User dropdown opens and closes
- [ ] Click outside closes menus
- [ ] Escape key closes menus
- [ ] Profile avatar displays correctly
- [ ] Fallback initial shows when no avatar
- [ ] Navbar shows shadow on scroll
- [ ] Logout link works
- [ ] Profile link works
- [ ] All navigation links work
- [ ] Responsive at all breakpoints
- [ ] Works with and without profile data

## Related Files

- `/templates/partials/navbar.html` - Navbar component template
- `/static/js/navbar.js` - Navbar JavaScript module
- `/templates/base/base.html` - Base template that includes navbar
- `/docs/design-system.md` - Design System documentation
