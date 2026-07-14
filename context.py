"""
Builds the context string that gets passed to the AI chatbot,
so it always answers based on the actual property numbers.
"""


def build_context(inputs: dict, metrics: dict, risk: dict) -> str:
    flags_text = "; ".join(risk["flags"]) if risk["flags"] else "None"

    return f"""
PROPERTY DETAILS
- Purchase Price: PKR {inputs['purchase_price']:,.0f}
- Down Payment: PKR {inputs['down_payment']:,.0f}
- Monthly Rent: PKR {inputs['monthly_rent']:,.0f}
- Vacancy Rate: {inputs['vacancy_rate']*100:.1f}%
- Property Tax (annual): PKR {inputs['property_tax']:,.0f}
- Insurance (annual): PKR {inputs['insurance']:,.0f}
- Maintenance (annual): PKR {inputs['maintenance']:,.0f}
- Utilities (annual): PKR {inputs['utilities']:,.0f}
- Management Fee (annual): PKR {inputs['management_fee']:,.0f}
- Other Expenses (annual): PKR {inputs['other_expenses']:,.0f}

CALCULATED METRICS
- NOI: PKR {metrics['noi']:,.0f}
- Cash Flow: PKR {metrics['cash_flow']:,.0f}
- Cap Rate: {metrics['cap_rate']*100:.2f}%
- ROI: {metrics['roi']*100:.2f}%

RISK ASSESSMENT
- Risk Level: {risk['level']}
- Risk Flags: {flags_text}
""".strip()
