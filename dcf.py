"""
Optional: Discounted Cash Flow (DCF) analysis.
"""


def calculate_dcf(annual_cash_flows: list[float], discount_rate: float) -> float:
    """
    annual_cash_flows: list of projected cash flows, one per year, e.g. [12000, 12500, 13000]
    discount_rate: decimal, e.g. 0.08 for 8%

    Returns the present value (sum of discounted cash flows).
    """
    present_value = 0.0
    for year, cash_flow in enumerate(annual_cash_flows, start=1):
        present_value += cash_flow / ((1 + discount_rate) ** year)
    return present_value
