"""
Plotly chart builders used by the dashboard.
"""

import plotly.graph_objects as go


def income_vs_expense_chart(gross_income: float, operating_expenses: float) -> go.Figure:
    fig = go.Figure(data=[
        go.Bar(name="Income", x=["Annual"], y=[gross_income], marker_color="#2E7D32"),
        go.Bar(name="Expenses", x=["Annual"], y=[operating_expenses], marker_color="#C62828"),
    ])
    fig.update_layout(title="Income vs Expenses", barmode="group", height=350)
    return fig


def cash_flow_chart(cash_flow: float) -> go.Figure:
    color = "#2E7D32" if cash_flow >= 0 else "#C62828"
    fig = go.Figure(data=[go.Bar(x=["Annual Cash Flow"], y=[cash_flow], marker_color=color)])
    fig.update_layout(title="Cash Flow", height=350)
    return fig


def expense_breakdown_chart(expenses: dict) -> go.Figure:
    """
    expenses: dict like {"Property Tax": 3000, "Insurance": 1200, ...}
    """
    labels = list(expenses.keys())
    values = list(expenses.values())
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
    fig.update_layout(title="Expense Breakdown", height=350)
    return fig
