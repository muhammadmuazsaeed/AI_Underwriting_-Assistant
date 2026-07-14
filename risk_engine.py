"""
Rule-based Risk Engine.
Takes the calculated metrics and returns a risk level + the reasons behind it.
"""


def assess_risk(vacancy_rate: float, roi: float, cap_rate: float, cash_flow: float, expense_ratio: float) -> dict:
    """
    All rate inputs are decimals (0.05 = 5%).
    expense_ratio = operating_expenses / gross_income

    Returns:
        {
            "level": "Low" | "Medium" | "High",
            "flags": [list of triggered warning strings]
        }
    """
    flags = []

    if vacancy_rate > 0.10:
        flags.append("High vacancy rate (above 10%)")

    if roi < 0.06:
        flags.append("Low ROI (below 6%)")

    if expense_ratio > 0.50:
        flags.append("High operating expenses (above 50% of income)")

    if cap_rate < 0.04:
        flags.append("Low cap rate (below 4%)")

    if cash_flow < 0:
        flags.append("Negative cash flow")

    # Decide overall level based on number of flags triggered
    if cash_flow < 0 or len(flags) >= 3:
        level = "High"
    elif len(flags) >= 1:
        level = "Medium"
    else:
        level = "Low"

    return {"level": level, "flags": flags}


RISK_COLORS = {
    "Low": "\U0001F7E2",     # green circle
    "Medium": "\U0001F7E1",  # yellow circle
    "High": "\U0001F534",    # red circle
}
