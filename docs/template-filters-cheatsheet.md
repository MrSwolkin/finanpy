# Template Filters - Quick Reference

## Load Filters

```django
{% load currency_filters %}
```

## Filters Cheatsheet

| Filter | Input | Output | Usage |
|--------|-------|--------|-------|
| `currency` | `1234.56` | `R$ 1.234,56` | `{{ amount\|currency }}` |
| `currency` | `-1234.56` | `-R$ 1.234,56` | `{{ amount\|currency }}` |
| `currency_abs` | `-1234.56` | `R$ 1.234,56` | `{{ amount\|currency_abs }}` |
| `date_br` | `2024-01-15` | `15/01/2024` | `{{ date\|date_br }}` |
| `datetime_br` | `2024-01-15 14:30` | `15/01/2024 14:30` | `{{ datetime\|datetime_br }}` |
| `number_format` | `1234567.89` | `1.234.567,89` | `{{ value\|number_format:2 }}` |
| `number_format` | `1234567` | `1.234.567` | `{{ value\|number_format:0 }}` |
| `percentage` | `0.156` | `15,6%` | `{{ rate\|percentage:1 }}` |
| `percentage` | `45.5` | `45,5%` | `{{ rate\|percentage:1 }}` |

## Common Patterns

### Transaction Amount

```django
<td class="{% if transaction.transaction_type == 'income' %}text-green-400{% else %}text-red-400{% endif %}">
  {% if transaction.transaction_type == 'income' %}+{% else %}-{% endif %}
  {{ transaction.amount|currency_abs }}
</td>
```

### Summary Cards

```django
<h3 class="text-green-400">{{ total_income|currency }}</h3>
<h3 class="text-red-400">{{ total_expenses|currency_abs }}</h3>
```

### Report Table

```django
<tr>
  <td>{{ item.date|date_br }}</td>
  <td>{{ item.description }}</td>
  <td>{{ item.amount|currency }}</td>
  <td>{{ item.percentage|percentage:1 }}</td>
</tr>
```

## Migration Guide

| Old | New |
|-----|-----|
| `R$ {{ amount\|floatformat:2 }}` | `{{ amount\|currency }}` |
| `{{ date\|date:"d/m/Y" }}` | `{{ date\|date_br }}` |
| `{{ datetime\|date:"d/m/Y H:i" }}` | `{{ datetime\|datetime_br }}` |

## Error Handling

| Input | Filter | Result |
|-------|--------|--------|
| `None` | `currency` | `R$ 0,00` |
| `""` | `currency` | `R$ 0,00` |
| `None` | `date_br` | `""` |
| Invalid | Any | Safe default |

## Parameters

### `number_format:N`
- `N` = number of decimal places
- Default: 2

### `percentage:N`
- `N` = number of decimal places
- Default: 1

## Examples

```django
{% load currency_filters %}

<!-- Balance -->
{{ account.balance|currency }}

<!-- Transaction Date -->
{{ transaction.date|date_br }}

<!-- Created Timestamp -->
{{ record.created_at|datetime_br }}

<!-- Count (no decimals) -->
{{ count|number_format:0 }}

<!-- Rate (2 decimals) -->
{{ growth_rate|percentage:2 }}

<!-- Conditional Color -->
<span class="{% if balance >= 0 %}text-green-400{% else %}text-red-400{% endif %}">
  {{ balance|currency }}
</span>
```

## Full Documentation

- **Quick Start:** `/core/templatetags/README.md`
- **Complete Guide:** `/docs/template-filters.md`
- **Examples:** `/docs/template-filters-example.html`
