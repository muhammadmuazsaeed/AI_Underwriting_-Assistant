"""
Cash Flow calculation.
"""


def calculate_annual_debt_service(loan_amount: float, annual_interest_rate: float, loan_term_years: int) -> float:
    """
    Simple annual mortgage payment estimate using standard amortization formula.
    If loan_amount is 0 (all-cash purchase), returns 0.
    """
    if loan_amount <= 0:
        return 0.0

    monthly_rate = annual_interest_rate / 12
    n_payments = loan_term_years * 12

    if monthly_rate == 0:
        monthly_payment = loan_amount / n_payments
    else:
        monthly_payment = loan_amount * (
            monthly_rate * (1 + monthly_rate) ** n_payments
        ) / ((1 + monthly_rate) ** n_payments - 1)

    return monthly_payment * 12


def calculate_cash_flow(noi: float, annual_debt_service: float) -> float:
    """
    Cash Flow = NOI - Annual Debt Service (mortgage payments)
    If the property is bought all-cash, annual_debt_service = 0.
    """
    return noi - annual_debt_service
