"""
Template filters for currency and date formatting.

These filters provide Brazilian locale formatting for:
- Currency values (R$)
- Dates and datetimes
- Numbers with thousands separators
- Percentages
"""
from django import template
from decimal import Decimal, InvalidOperation
from datetime import date, datetime

register = template.Library()


@register.filter(name='currency')
def currency(value):
    """
    Formata um número como moeda brasileira (Real).

    Exemplos:
        1234.56 -> R$ 1.234,56
        -1234.56 -> -R$ 1.234,56
        None -> R$ 0,00

    Args:
        value: Número para formatar (Decimal, float, int ou string)

    Returns:
        String formatada como moeda brasileira
    """
    # Handle None or empty values
    if value is None or value == '':
        return 'R$ 0,00'

    try:
        # Convert to Decimal for precise calculation
        if isinstance(value, str):
            value = value.replace(',', '.')
        decimal_value = Decimal(str(value))

        # Check if negative
        is_negative = decimal_value < 0
        absolute_value = abs(decimal_value)

        # Format with 2 decimal places
        formatted = f'{absolute_value:,.2f}'

        # Replace default separators with Brazilian format
        # English: 1,234.56 -> Brazilian: 1.234,56
        formatted = formatted.replace(',', 'TEMP')
        formatted = formatted.replace('.', ',')
        formatted = formatted.replace('TEMP', '.')

        # Add currency symbol
        if is_negative:
            return f'-R$ {formatted}'
        return f'R$ {formatted}'

    except (ValueError, InvalidOperation, TypeError):
        return 'R$ 0,00'


@register.filter(name='currency_abs')
def currency_abs(value):
    """
    Formata o valor absoluto como moeda (sem sinal negativo).

    Exemplos:
        -1234.56 -> R$ 1.234,56
        1234.56 -> R$ 1.234,56

    Args:
        value: Número para formatar

    Returns:
        String formatada como moeda brasileira sem sinal
    """
    # Handle None or empty values
    if value is None or value == '':
        return 'R$ 0,00'

    try:
        # Convert to Decimal and get absolute value
        if isinstance(value, str):
            value = value.replace(',', '.')
        decimal_value = abs(Decimal(str(value)))

        # Format with 2 decimal places
        formatted = f'{decimal_value:,.2f}'

        # Replace default separators with Brazilian format
        formatted = formatted.replace(',', 'TEMP')
        formatted = formatted.replace('.', ',')
        formatted = formatted.replace('TEMP', '.')

        return f'R$ {formatted}'

    except (ValueError, InvalidOperation, TypeError):
        return 'R$ 0,00'


@register.filter(name='date_br')
def date_br(value):
    """
    Formata uma data no formato brasileiro.

    Exemplos:
        2024-01-15 -> 15/01/2024
        datetime(2024, 1, 15) -> 15/01/2024

    Args:
        value: Data para formatar (date ou datetime)

    Returns:
        String formatada no padrão brasileiro DD/MM/YYYY
    """
    if value is None or value == '':
        return ''

    try:
        # Handle both date and datetime objects
        if isinstance(value, (date, datetime)):
            return value.strftime('%d/%m/%Y')

        # Try to parse string dates
        if isinstance(value, str):
            # Try common formats
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']:
                try:
                    dt = datetime.strptime(value, fmt)
                    return dt.strftime('%d/%m/%Y')
                except ValueError:
                    continue

        return ''

    except (ValueError, TypeError, AttributeError):
        return ''


@register.filter(name='datetime_br')
def datetime_br(value):
    """
    Formata um datetime no formato brasileiro.

    Exemplos:
        2024-01-15 14:30:00 -> 15/01/2024 14:30
        datetime(2024, 1, 15, 14, 30) -> 15/01/2024 14:30

    Args:
        value: Datetime para formatar

    Returns:
        String formatada no padrão brasileiro DD/MM/YYYY HH:MM
    """
    if value is None or value == '':
        return ''

    try:
        # Handle datetime objects
        if isinstance(value, datetime):
            return value.strftime('%d/%m/%Y %H:%M')

        # Handle date objects (add 00:00 time)
        if isinstance(value, date):
            return value.strftime('%d/%m/%Y 00:00')

        # Try to parse string datetimes
        if isinstance(value, str):
            # Try common formats
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M']:
                try:
                    dt = datetime.strptime(value, fmt)
                    return dt.strftime('%d/%m/%Y %H:%M')
                except ValueError:
                    continue

            # Try date-only format
            try:
                dt = datetime.strptime(value, '%Y-%m-%d')
                return dt.strftime('%d/%m/%Y 00:00')
            except ValueError:
                pass

        return ''

    except (ValueError, TypeError, AttributeError):
        return ''


@register.filter(name='number_format')
def number_format(value, decimal_places=2):
    """
    Formata um número com separador de milhares e casas decimais.

    Exemplos:
        (1234567.89, 2) -> 1.234.567,89
        (1234567.89, 0) -> 1.234.568
        (1234.5, 3) -> 1.234,500

    Args:
        value: Número para formatar
        decimal_places: Número de casas decimais (padrão: 2)

    Returns:
        String formatada com separadores brasileiros
    """
    if value is None or value == '':
        return '0'

    try:
        # Convert to Decimal
        if isinstance(value, str):
            value = value.replace(',', '.')
        decimal_value = Decimal(str(value))

        # Convert decimal_places to int if needed
        try:
            decimal_places = int(decimal_places)
        except (ValueError, TypeError):
            decimal_places = 2

        # Format with specified decimal places
        format_string = f'{{:,.{decimal_places}f}}'
        formatted = format_string.format(decimal_value)

        # Replace default separators with Brazilian format
        formatted = formatted.replace(',', 'TEMP')
        formatted = formatted.replace('.', ',')
        formatted = formatted.replace('TEMP', '.')

        return formatted

    except (ValueError, InvalidOperation, TypeError):
        return '0'


@register.filter(name='percentage')
def percentage(value, decimal_places=1):
    """
    Formata um número como porcentagem.

    Exemplos:
        (0.156, 1) -> 15,6%
        (45.5, 1) -> 45,5%
        (0.156, 2) -> 15,60%
        (100, 0) -> 100%

    Args:
        value: Número para formatar (pode ser fração 0.156 ou já em porcentagem 15.6)
        decimal_places: Número de casas decimais (padrão: 1)

    Returns:
        String formatada como porcentagem
    """
    if value is None or value == '':
        return '0%'

    try:
        # Convert to Decimal
        if isinstance(value, str):
            value = value.replace(',', '.')
        decimal_value = Decimal(str(value))

        # If value is between -1 and 1 (excluding 0), assume it's a fraction and multiply by 100
        # This handles both 0.156 -> 15.6% and 45.5 -> 45.5%
        if -1 < decimal_value < 1 and decimal_value != 0:
            decimal_value = decimal_value * 100

        # Convert decimal_places to int if needed
        try:
            decimal_places = int(decimal_places)
        except (ValueError, TypeError):
            decimal_places = 1

        # Format with specified decimal places
        format_string = f'{{:,.{decimal_places}f}}'
        formatted = format_string.format(decimal_value)

        # Replace default separators with Brazilian format
        formatted = formatted.replace(',', 'TEMP')
        formatted = formatted.replace('.', ',')
        formatted = formatted.replace('TEMP', '.')

        return f'{formatted}%'

    except (ValueError, InvalidOperation, TypeError):
        return '0%'
