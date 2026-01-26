# Template Filters Documentation

## Overview

Finanpy provides custom Django template filters for formatting currency, dates, numbers, and percentages according to Brazilian locale standards.

## Installation

The filters are automatically available in the `core` app. To use them in your templates:

```django
{% load currency_filters %}
```

## Available Filters

### 1. currency

Formats a number as Brazilian Real currency (R$).

**Syntax:** `{{ value|currency }}`

**Examples:**

```django
{{ 1234.56|currency }}           {# Output: R$ 1.234,56 #}
{{ -1234.56|currency }}          {# Output: -R$ 1.234,56 #}
{{ transaction.amount|currency }} {# Output: R$ 1.000.000,99 #}
```

**Input types:** Decimal, float, int, string
**Handles:** None, empty strings, negative values
**Default for invalid input:** R$ 0,00

---

### 2. currency_abs

Formats the absolute value as currency (without negative sign).

**Syntax:** `{{ value|currency_abs }}`

**Examples:**

```django
{{ -1234.56|currency_abs }}      {# Output: R$ 1.234,56 #}
{{ 1234.56|currency_abs }}       {# Output: R$ 1.234,56 #}
```

**Use case:** Display amounts without sign (useful for expense lists where the color indicates positive/negative)

---

### 3. date_br

Formats a date in Brazilian format (DD/MM/YYYY).

**Syntax:** `{{ date_value|date_br }}`

**Examples:**

```django
{{ transaction.date|date_br }}   {# Output: 15/01/2024 #}
{{ account.created_at|date_br }} {# Output: 15/01/2024 #}
```

**Input types:** date, datetime, string (ISO format or Brazilian format)
**Output format:** DD/MM/YYYY
**Default for invalid input:** empty string

---

### 4. datetime_br

Formats a datetime in Brazilian format (DD/MM/YYYY HH:MM).

**Syntax:** `{{ datetime_value|datetime_br }}`

**Examples:**

```django
{{ transaction.created_at|datetime_br }}  {# Output: 15/01/2024 14:30 #}
{{ user.last_login|datetime_br }}         {# Output: 15/01/2024 09:05 #}
```

**Input types:** datetime, date, string
**Output format:** DD/MM/YYYY HH:MM
**Default for invalid input:** empty string

---

### 5. number_format

Formats a number with thousands separator and specified decimal places.

**Syntax:** `{{ value|number_format:decimal_places }}`

**Examples:**

```django
{{ 1234567.89|number_format:2 }}    {# Output: 1.234.567,89 #}
{{ 1234567.89|number_format:0 }}    {# Output: 1.234.568 #}
{{ balance|number_format:3 }}       {# Output: 1.234,500 #}
{{ count|number_format:0 }}         {# Output: 1.234 #}
```

**Parameters:**
- `decimal_places` (optional): Number of decimal places (default: 2)

**Use case:** Formatting large numbers, quantities, or custom precision values

---

### 6. percentage

Formats a number as a percentage with Brazilian decimal format.

**Syntax:** `{{ value|percentage:decimal_places }}`

**Examples:**

```django
{{ 0.156|percentage:1 }}      {# Output: 15,6% #}
{{ 0.156|percentage:2 }}      {# Output: 15,60% #}
{{ 45.5|percentage:1 }}       {# Output: 45,5% #}
{{ growth_rate|percentage:1 }} {# Output: 23,4% #}
```

**Parameters:**
- `decimal_places` (optional): Number of decimal places (default: 1)

**Smart behavior:**
- If value is between -1 and 1 (e.g., 0.156), multiplies by 100
- If value is already a percentage (e.g., 45.5), uses as-is

---

## Common Usage Patterns

### Transaction List

```django
{% load currency_filters %}

<div class="transaction-item">
    <span class="date">{{ transaction.date|date_br }}</span>
    <span class="description">{{ transaction.description }}</span>
    <span class="amount {% if transaction.amount < 0 %}text-red-400{% else %}text-green-400{% endif %}">
        {{ transaction.amount|currency }}
    </span>
</div>
```

### Account Balance

```django
{% load currency_filters %}

<div class="account-card">
    <h3>{{ account.name }}</h3>
    <div class="balance">
        <span class="label">Saldo:</span>
        <span class="value">{{ account.balance|currency }}</span>
    </div>
    <div class="last-updated">
        Atualizado em: {{ account.updated_at|datetime_br }}
    </div>
</div>
```

### Dashboard Statistics

```django
{% load currency_filters %}

<div class="stats-grid">
    <div class="stat-card">
        <h4>Receitas</h4>
        <p class="value text-green-400">{{ total_income|currency }}</p>
    </div>
    <div class="stat-card">
        <h4>Despesas</h4>
        <p class="value text-red-400">{{ total_expenses|currency_abs }}</p>
    </div>
    <div class="stat-card">
        <h4>Taxa de Poupança</h4>
        <p class="value">{{ savings_rate|percentage:1 }}</p>
    </div>
</div>
```

### Reports with Numbers

```django
{% load currency_filters %}

<table class="report-table">
    <thead>
        <tr>
            <th>Categoria</th>
            <th>Total</th>
            <th>% do Total</th>
            <th>Transações</th>
        </tr>
    </thead>
    <tbody>
        {% for category in categories %}
        <tr>
            <td>{{ category.name }}</td>
            <td>{{ category.total|currency }}</td>
            <td>{{ category.percentage|percentage:1 }}</td>
            <td>{{ category.count|number_format:0 }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

## Brazilian Locale Standards

All filters follow Brazilian formatting conventions:

- **Thousands separator:** `.` (dot)
- **Decimal separator:** `,` (comma)
- **Currency symbol:** `R$` (before the amount)
- **Date format:** `DD/MM/YYYY`
- **Time format:** `HH:MM` (24-hour)
- **Percentage:** `value%` with comma as decimal separator

## Error Handling

All filters are designed to be safe and never raise exceptions:

- **Invalid input:** Returns a sensible default (R$ 0,00, empty string, or 0)
- **None values:** Handled gracefully
- **Type errors:** Caught and defaulted
- **String conversion:** Automatically handles comma/dot in string inputs

## Performance Notes

- Uses Python's `Decimal` type for precise financial calculations
- Efficient string replacement for locale formatting
- No external dependencies (locale module not required)
- Safe for use in large lists/tables

## Testing

Run the test suite to verify filter behavior:

```bash
python test_filters.py
```

This tests all filters with various input types and edge cases.
