"""
Capitalization Rate (Cap Rate) calculation.
"""


def calculate_cap_rate(noi: float, purchase_price: float) -> float:
    """
    Cap Rate = NOI / Purchase Price
    Returns a decimal (e.g. 0.065 for 6.5%). Multiply by 100 to display as %.
    """
    if purchase_price <= 0:
        return 0.0
    return noi / purchase_price
