# Changelog

All notable changes to the Finanpy project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-27

### Added

#### User Authentication (Sprint 1)
- Custom user model with email-based authentication
- User registration with automatic login
- Login/logout functionality
- Password reset workflow with email support
- Welcome and farewell messages via Django messages framework

#### User Profile (Sprint 2)
- Profile model with OneToOne relationship to User
- First name, last name, and phone fields
- Avatar upload with image validation
- Auto-created profile on user registration via signals

#### Bank Accounts (Sprint 3)
- Account model with multiple types (checking, savings, investment, other)
- Initial and current balance tracking
- Active/inactive status
- CRUD operations with ownership validation
- Transaction count warning on deletion

#### Categories (Sprint 4)
- Category model with income/expense types
- Color customization (hex format)
- Default categories created on user registration
- Protection against editing/deleting default categories
- Transaction count validation before deletion

#### Transactions (Sprint 5)
- Transaction model linking accounts and categories
- Automatic account balance updates via signals
- Support for income and expense types
- Transaction date with smart validation
- Future transaction support with warnings
- Date filtering (date range, type, category, account)
- Pagination (20 items per page)

#### Dashboard (Sprint 6)
- Total balance calculation across all accounts
- Period-based filtering (current month, last month, quarterly, yearly, custom)
- Income vs expense breakdown
- Top 5 expense categories
- Recent transactions quick view (last 5)

#### Landing Page (Sprint 7)
- Public landing page for unauthenticated users
- Automatic redirect to dashboard for logged-in users
- Hero section with call-to-action
- Benefits and features sections

#### Navbar and Layout (Sprint 8)
- Responsive navigation bar
- User dropdown menu with profile and logout
- Mobile hamburger menu
- Sticky header with backdrop blur
- Footer partial

#### UX Improvements (Sprint 9)
- Delete confirmation dialogs
- Success/error messages with proper styling
- Loading states on form submissions
- Real-time form validation
- Tooltips and help text

#### Accessibility (Sprint 9)
- ARIA labels on interactive elements
- Proper form labels with for/id attributes
- WCAG AA color contrast compliance
- Keyboard navigation support
- Alt text on images

#### Performance (Sprint 9)
- Query optimization with select_related/prefetch_related
- Database indexes on frequently queried fields
- Efficient pagination
- Lazy loading for images

#### Responsiveness (Sprint 9)
- Mobile-first design approach
- Tested on 375px, 768px, 1024px+ viewports
- Cross-browser compatibility (Chrome, Firefox, Safari, Edge)

#### Refinements (Sprint 10)
- Custom template filter for Brazilian currency (R$ 1.234,56)
- Date formatting in Brazilian format (dd/mm/yyyy)
- Account deletion validation with transaction count
- Category deletion protection when transactions exist
- Negative value validation with contextual messages
- Future date validation with warning system

### Technical Features

#### Architecture
- Django 6+ with Class-Based Views
- TailwindCSS 4 via django-tailwind
- SQLite database (development)
- Custom user model extending AbstractUser
- Signal-based automation (profile creation, balance updates)

#### Security
- LoginRequiredMixin on all protected views
- User data isolation (queries filtered by request.user)
- CSRF protection enabled
- Password validation rules
- Open redirect prevention

#### Code Quality
- PEP8 compliant code style
- English code, Portuguese (pt-BR) interface
- Comprehensive docstrings
- Type hints on key functions
- Conventional commit messages

### Project Structure

```
finanpy/
├── core/           # Project settings, DashboardView, template filters
├── users/          # Custom user authentication
├── profiles/       # User profile management
├── accounts/       # Bank account CRUD
├── categories/     # Transaction category management
├── transactions/   # Financial transaction CRUD with filtering
├── theme/          # TailwindCSS configuration
├── templates/      # Global templates and partials
├── static/         # JavaScript and images
├── media/          # User uploads (avatars)
└── docs/           # Project documentation
```

---

## [Unreleased]

### Planned
- Chart.js integration for visual analytics (Task 34.6)
- Automated test suite with pytest-django (Sprint 11)
- Docker containerization (Sprint 12)
- Production deployment configuration

---

*Finanpy - Personal Finance Management*
