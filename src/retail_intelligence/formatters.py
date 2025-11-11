"""
Formatters for Indian retail data
Handles INR currency and quantity formatting
"""

from typing import Union, Optional, Dict, Any, List


def format_inr(amount: Union[int, float], decimals: int = 0) -> str:
    """
    Format amount in Indian Rupee format with lakhs/crores

    Args:
        amount: Amount to format
        decimals: Number of decimal places

    Returns:
        Formatted INR string

    Examples:
        >>> format_inr(1500)
        '₹1,500'
        >>> format_inr(150000)
        '₹1.50 Lakh'
        >>> format_inr(10000000)
        '₹1.00 Cr'
    """
    if amount < 0:
        sign = "-"
        amount = abs(amount)
    else:
        sign = ""

    # Crores (10 million+)
    if amount >= 10000000:
        value = amount / 10000000
        formatted = f"{sign}₹{value:.{decimals}f} Cr"

    # Lakhs (100,000 - 9,999,999)
    elif amount >= 100000:
        value = amount / 100000
        formatted = f"{sign}₹{value:.{decimals}f} Lakh"

    # Thousands with commas
    elif amount >= 1000:
        formatted = f"{sign}₹{amount:,.{decimals}f}"

    # Less than 1000
    else:
        formatted = f"{sign}₹{amount:.{decimals}f}"

    # Clean up trailing zeros if decimals=0
    if decimals == 0:
        formatted = formatted.replace(".0 ", " ").replace(".00 ", " ")

    return formatted


def format_quantity(
    quantity: Union[int, float], unit: str = "units", decimals: int = 0
) -> str:
    """
    Format quantity with appropriate units

    Args:
        quantity: Quantity to format
        unit: Unit name (units, pieces, kg, items, etc.)
        decimals: Number of decimal places

    Returns:
        Formatted quantity string

    Examples:
        >>> format_quantity(1500, "pieces")
        '1,500 pieces'
        >>> format_quantity(250.5, "kg", 1)
        '250.5 kg'
    """
    if quantity >= 100000:
        # Use lakhs for large quantities
        value = quantity / 100000
        return f"{value:.{decimals}f} Lakh {unit}"
    elif quantity >= 1000:
        # Use commas for thousands
        return f"{quantity:,.{decimals}f} {unit}"
    else:
        return f"{quantity:.{decimals}f} {unit}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format percentage value

    Args:
        value: Percentage value (e.g., 15.5 for 15.5%)
        decimals: Number of decimal places

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(15.5)
        '15.5%'
        >>> format_percentage(8.234, 2)
        '8.23%'
    """
    return f"{value:.{decimals}f}%"


def format_growth(current: float, previous: float, decimals: int = 1) -> str:
    """
    Calculate and format growth percentage

    Args:
        current: Current period value
        previous: Previous period value
        decimals: Number of decimal places

    Returns:
        Formatted growth string with arrow

    Examples:
        >>> format_growth(110, 100)
        '↑ 10.0%'
        >>> format_growth(95, 100)
        '↓ 5.0%'
    """
    if previous == 0:
        return "N/A"

    growth = ((current - previous) / previous) * 100

    if growth > 0:
        arrow = "↑"
    elif growth < 0:
        arrow = "↓"
        growth = abs(growth)
    else:
        arrow = "→"

    return f"{arrow} {growth:.{decimals}f}%"


def format_date_indian(date_obj, format_type: str = "short") -> str:
    """
    Format date in Indian format

    Args:
        date_obj: datetime object
        format_type: 'short' (DD-MMM-YYYY) or 'long' (DD Month YYYY)

    Returns:
        Formatted date string

    Examples:
        >>> format_date_indian(datetime(2025, 11, 15), "short")
        '15-Nov-2025'
    """
    if format_type == "short":
        return date_obj.strftime("%d-%b-%Y")
    else:
        return date_obj.strftime("%d %B %Y")


def format_metric_summary(
    metric_name: str,
    value: Union[int, float],
    unit_type: str = "inr",
    growth: Optional[float] = None,
) -> str:
    """
    Format a metric with name, value, and optional growth

    Args:
        metric_name: Name of the metric
        value: Metric value
        unit_type: 'inr', 'quantity', or 'percentage'
        growth: Optional growth percentage

    Returns:
        Formatted metric string

    Examples:
        >>> format_metric_summary("Total Sales", 1500000, "inr", 15.5)
        'Total Sales: ₹15.00 Lakh (↑ 15.5%)'
    """
    if unit_type == "inr":
        formatted_value = format_inr(value)
    elif unit_type == "percentage":
        formatted_value = format_percentage(value)
    else:
        formatted_value = format_quantity(value, "units")

    if growth is not None:
        growth_str = (
            f" ({format_growth(value, value / (1 + growth / 100))})"
            if growth != 0
            else ""
        )
    else:
        growth_str = ""

    return f"{metric_name}: {formatted_value}{growth_str}"


from typing import Optional
