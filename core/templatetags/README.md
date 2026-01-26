# Currency Filters - Template Tags

## Overview

Custom Django template filters for formatting currency, dates, numbers, and percentages according to Brazilian locale standards (pt-BR).

## Quick Start

Add this line at the top of your template:

```django
{% load currency_filters %}
```

## Filters Reference

### `currency`

Format a number as Brazilian Real (R$).

```django
{{ 1234.56|currency }}
```
**Output:** `R$ 1.234,56`

**Features:**
- Adds thousands separator (.)
- Uses comma for decimals (,)
- Handles negative values: `-R$ 1.234,56`
- Safe for None/empty values: returns `R$ 0,00`

---

### `currency_abs`

Format absolute value as currency (no negative sign).

```django
{{ -1234.56|currency_abs }}
```
**Output:** `R$ 1.234,56`

**Use case:** Display expenses without negative sign when color already indicates the type.

---

### `date_br`

Format date in Brazilian format.

```django
{{ transaction.date|date_br }}
```
**Output:** `15/01/2024`

**Accepts:** date, datetime, ISO string

---

### `datetime_br`

Format datetime in Brazilian format.

```django
{{ transaction.created_at|datetime_br }}
```
**Output:** `15/01/2024 14:30`

**Accepts:** datetime, date, ISO string

---

### `number_format`

Format number with thousands separator and custom decimal places.

```django
{{ 1234567.89|number_format:2 }}
```
**Output:** `1.234.567,89`

**Parameter:** decimal_places (default: 2)

**Examples:**
```django
{{ count|number_format:0 }}     → 1.234
{{ amount|number_format:3 }}    → 1.234,567
```

---

### `percentage`

Format as percentage with Brazilian decimal format.

```django
{{ 0.156|percentage:1 }}
```
**Output:** `15,6%`

**Smart behavior:**
- Values between -1 and 1: multiplies by 100
- Other values: uses as-is

**Examples:**
```django
{{ 0.156|percentage:1 }}    → 15,6%
{{ 45.5|percentage:1 }}     → 45,5%
{{ 0.5|percentage:2 }}      → 50,00%
```

---

## Migration Guide

### Replacing floatformat

**Before:**
```django
R$ {{ amount|floatformat:2 }}
```

**After:**
```django
{{ amount|currency }}
```

### Replacing date filter

**Before:**
```django
{{ transaction.date|date:"d/m/Y" }}
```

**After:**
```django
{{ transaction.date|date_br }}
```

## Common Patterns

### Transaction List

```django
{% load currency_filters %}

{% for transaction in transactions %}
  <tr>
    <td>{{ transaction.transaction_date|date_br }}</td>
    <td>{{ transaction.description }}</td>
    <td class="{% if transaction.transaction_type == 'income' %}text-green-400{% else %}text-red-400{% endif %}">
      {% if transaction.transaction_type == 'income' %}+{% else %}-{% endif %}
      {{ transaction.amount|currency_abs }}
    </td>
  </tr>
{% endfor %}
```

### Summary Cards

```django
{% load currency_filters %}

<!-- Income -->
<h3 class="text-green-400">{{ total_income|currency }}</h3>

<!-- Expenses -->
<h3 class="text-red-400">{{ total_expenses|currency_abs }}</h3>

<!-- Balance -->
<h3 class="{% if balance >= 0 %}text-green-400{% else %}text-red-400{% endif %}">
  {{ balance|currency }}
</h3>
```

### Reports with Percentages

```django
{% load currency_filters %}

<table>
  {% for category in categories %}
  <tr>
    <td>{{ category.name }}</td>
    <td>{{ category.total|currency }}</td>
    <td>{{ category.percentage|percentage:1 }}</td>
    <td>{{ category.count|number_format:0 }}</td>
  </tr>
  {% endfor %}
</table>
```

## Error Handling

All filters are safe and never raise exceptions:

| Input | Filter | Output |
|-------|--------|--------|
| `None` | `currency` | `R$ 0,00` |
| `""` | `currency` | `R$ 0,00` |
| `None` | `date_br` | `""` (empty) |
| `None` | `percentage` | `0%` |
| Invalid value | `currency` | `R$ 0,00` |

## Technical Details

### Input Types Supported

- **currency/currency_abs:** Decimal, float, int, string
- **date_br:** date, datetime, string (ISO or Brazilian format)
- **datetime_br:** datetime, date, string
- **number_format:** Decimal, float, int, string
- **percentage:** Decimal, float, int, string

### Decimal Precision

Uses Python's `Decimal` type for financial calculations to avoid floating-point errors.

### Locale Format

Follows Brazilian standards:
- Thousands: `.` (dot)
- Decimals: `,` (comma)
- Currency: `R$`
- Date: `DD/MM/YYYY`
- Time: `HH:MM` (24-hour)

## Testing

Run the test suite:

```bash
python test_filters.py
```

## Full Documentation

See `/docs/template-filters.md` for complete documentation with examples.
