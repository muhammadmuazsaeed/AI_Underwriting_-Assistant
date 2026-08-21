"""
Net Operating Income (NOI) calculations.
"""


def calculate_gross_income(monthly_rent: float, vacancy_rate: float) -> float:
    """
    Annual Gross Rental Income after accounting for vacancy.
    vacancy_rate should be a decimal, e.g. 0.05 for 5%.
    """
    annual_rent = monthly_rent * 12
    return annual_rent * (1 - vacancy_rate)


def calculate_operating_expenses(
    property_tax: float,
    insurance: float,
    maintenance: float,
    utilities: float,
    management_fee: float,
    other_expenses: float,
) -> float:
    """
    Sum of all annual operating expenses.
    Assumes each input is already an ANNUAL figure.
    """
    return (
        property_tax
        + insurance
        + maintenance
        + utilities
        + management_fee
        + other_expenses
    )


def calculate_noi(gross_income: float, operating_expenses: float) -> float:
    """
    NOI = Gross Income - Operating Expenses
    """
    return gross_income - operating_expenses
