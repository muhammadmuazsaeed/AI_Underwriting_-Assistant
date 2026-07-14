"""
Return on Investment (ROI) calculation.
"""


def calculate_roi(annual_cash_flow: float, total_cash_invested: float) -> float:
    """
    ROI = Annual Cash Flow / Total Cash Invested (down payment + closing costs, etc.)
    Returns a decimal (e.g. 0.12 for 12%). Multiply by 100 to display as %.
    """
    if total_cash_invested <= 0:
        return 0.0
    return annual_cash_flow / total_cash_invested
