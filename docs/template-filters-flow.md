# Template Filters - Processing Flow

## Filter Processing Flow

### 1. Currency Filter

```
Input: 1234.56
  ↓
Check if None/empty → Yes → Return "R$ 0,00"
  ↓ No
Convert to Decimal
  ↓
Check if negative → Save sign
  ↓
Get absolute value
  ↓
Format with 2 decimals: "1,234.56"
  ↓
Replace separators:
  , → TEMP → "1TEMP234.56"
  . → ,    → "1TEMP234,56"
  TEMP → . → "1.234,56"
  ↓
Add currency symbol: "R$ 1.234,56"
  ↓
Add negative sign if needed: "-R$ 1.234,56"
  ↓
Output: "R$ 1.234,56"
```

### 2. Date BR Filter

```
Input: "2024-01-15"
  ↓
Check if None/empty → Yes → Return ""
  ↓ No
Check type:
  - date object → Use directly
  - datetime object → Use directly
  - string → Parse with strptime
  ↓
Format with strftime("%d/%m/%Y")
  ↓
Output: "15/01/2024"
```

### 3. Number Format Filter

```
Input: 1234567.89, decimal_places=2
  ↓
Check if None/empty → Yes → Return "0"
  ↓ No
Convert to Decimal
  ↓
Format with N decimal places: "1,234,567.89"
  ↓
Replace separators (Brazilian format):
  , → TEMP → "1TEMP234TEMP567.89"
  . → ,    → "1TEMP234TEMP567,89"
  TEMP → . → "1.234.567,89"
  ↓
Output: "1.234.567,89"
```

### 4. Percentage Filter

```
Input: 0.156, decimal_places=1
  ↓
Check if None/empty → Yes → Return "0%"
  ↓ No
Convert to Decimal
  ↓
Check if between -1 and 1 → Yes → Multiply by 100
  ↓
0.156 × 100 = 15.6
  ↓
Format with N decimal places: "15.6"
  ↓
Replace separators (Brazilian format):
  . → , → "15,6"
  ↓
Add % symbol: "15,6%"
  ↓
Output: "15,6%"
```

## Error Handling Flow

```
Try:
  ↓
  Process value
  ↓
  Return formatted result
  ↓
Catch Exception:
  - ValueError
  - InvalidOperation
  - TypeError
  ↓
  Return safe default:
    - currency: "R$ 0,00"
    - date: ""
    - number: "0"
    - percentage: "0%"
```

## Template Loading Flow

```
Template File
  ↓
{% load currency_filters %}
  ↓
Django searches for:
  1. core/templatetags/currency_filters.py
  ↓
Found → Load module
  ↓
Register all filters:
  - @register.filter(name='currency')
  - @register.filter(name='currency_abs')
  - @register.filter(name='date_br')
  - @register.filter(name='datetime_br')
  - @register.filter(name='number_format')
  - @register.filter(name='percentage')
  ↓
Filters available in template
  ↓
{{ value|currency }}
  ↓
Call currency() function
  ↓
Return formatted value
  ↓
Render in HTML
```

## Type Conversion Flow

```
Input Value
  ↓
Check type:
  ├─ None → Return default
  ├─ Empty string → Return default
  ├─ Decimal → Use directly
  ├─ Float → Convert to Decimal
  ├─ Int → Convert to Decimal
  └─ String → Clean and convert
       ↓
       Replace ',' with '.'
       ↓
       Convert to Decimal
       ↓
       If error → Return default
```

## Decimal Precision Flow (Financial Calculations)

```
Why use Decimal instead of float?

Float arithmetic:
  0.1 + 0.2 = 0.30000000000000004 ❌

Decimal arithmetic:
  Decimal('0.1') + Decimal('0.2') = Decimal('0.3') ✓

Flow:
  Input: float(1234.56)
    ↓
  Convert to string: "1234.56"
    ↓
  Convert to Decimal: Decimal('1234.56')
    ↓
  Perform calculations with precision
    ↓
  Format with exact decimal places
    ↓
  Output: "R$ 1.234,56"
```

## Brazilian Locale Separator Logic

```
English Format:  1,234.56
                  ↓   ↓
                  |   └─ Decimal separator (.)
                  └───── Thousands separator (,)

Brazilian Format: 1.234,56
                   ↓   ↓
                   |   └─ Decimal separator (,)
                   └───── Thousands separator (.)

Conversion Steps:
  1,234.56
    ↓ Replace ',' with 'TEMP'
  1TEMP234.56
    ↓ Replace '.' with ','
  1TEMP234,56
    ↓ Replace 'TEMP' with '.'
  1.234,56 ✓

Why use TEMP?
- Direct swap would cause conflict
- TEMP is a safe intermediate value
```

## Performance Flow

```
Single Filter Call:
  Template render
    ↓
  {{ value|currency }}
    ↓
  Call filter function (microseconds)
    ↓
  Return formatted string
    ↓
  Continue rendering
  Total: < 1ms per call

List of Items:
  {% for item in items %}
    ↓
  {{ item.amount|currency }}
    ↓ (repeated N times)
  {% endfor %}
  Total: ~N milliseconds

Optimization:
  - Filters are lightweight
  - No database queries
  - No external API calls
  - Pure Python string formatting
  - Caching not needed
```

## Integration Flow

```
Django Project
  ↓
core/
  └── templatetags/
       └── currency_filters.py
  ↓
Any Template
  ↓
{% load currency_filters %}
  ↓
Use filters anywhere in template
  ↓
{{ transaction.amount|currency }}
{{ transaction.date|date_br }}
{{ percentage|percentage:1 }}
  ↓
Rendered HTML with formatted values
```

## Migration Path

```
Old Template:
  R$ {{ amount|floatformat:2 }}
    ↓
Add load statement:
  {% load currency_filters %}
    ↓
Replace filter:
  {{ amount|currency }}
    ↓
Test in browser
    ↓
Verify formatting
    ↓
✓ Migration complete
```

## Complete Example Flow

```
View sends context:
  {
    'total_income': Decimal('1234.56'),
    'transaction_date': date(2024, 1, 15),
    'savings_rate': Decimal('0.156')
  }
  ↓
Template processes:
  {% load currency_filters %}

  <p>{{ total_income|currency }}</p>
  → "R$ 1.234,56"

  <p>{{ transaction_date|date_br }}</p>
  → "15/01/2024"

  <p>{{ savings_rate|percentage:1 }}</p>
  → "15,6%"
  ↓
HTML Output:
  <p>R$ 1.234,56</p>
  <p>15/01/2024</p>
  <p>15,6%</p>
  ↓
Browser renders formatted values
```
