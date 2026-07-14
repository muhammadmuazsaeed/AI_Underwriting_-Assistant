"""
Generates the PDF investment memo using ReportLab.
"""

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.units import inch


def generate_pdf_report(inputs: dict, metrics: dict, risk: dict, ai_summary: str) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.7 * inch, bottomMargin=0.7 * inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Heading1"], textColor=colors.HexColor("#1F3864")
    )
    heading_style = ParagraphStyle(
        "HeadingStyle", parent=styles["Heading2"], textColor=colors.HexColor("#2E75B6")
    )
    body_style = styles["BodyText"]

    elements = []

    elements.append(Paragraph("Investment Memo", title_style))
    elements.append(Paragraph("AI Underwriting Assistant", body_style))
    elements.append(Spacer(1, 20))

    # Property Info
    elements.append(Paragraph("Property Information", heading_style))
    property_table_data = [
        ["Purchase Price", f"PKR {inputs['purchase_price']:,.0f}"],
        ["Down Payment", f"PKR {inputs['down_payment']:,.0f}"],
        ["Monthly Rent", f"PKR {inputs['monthly_rent']:,.0f}"],
        ["Vacancy Rate", f"{inputs['vacancy_rate']*100:.1f}%"],
    ]
    elements.append(_make_table(property_table_data))
    elements.append(Spacer(1, 16))

    # Financial Metrics
    elements.append(Paragraph("Financial Metrics", heading_style))
    metrics_table_data = [
        ["NOI", f"PKR {metrics['noi']:,.0f}"],
        ["Cash Flow", f"PKR {metrics['cash_flow']:,.0f}"],
        ["Cap Rate", f"{metrics['cap_rate']*100:.2f}%"],
        ["ROI", f"{metrics['roi']*100:.2f}%"],
    ]
    elements.append(_make_table(metrics_table_data))
    elements.append(Spacer(1, 16))

    # Risk Assessment
    elements.append(Paragraph("Risk Assessment", heading_style))
    elements.append(Paragraph(f"<b>Risk Level:</b> {risk['level']}", body_style))
    if risk["flags"]:
        for flag in risk["flags"]:
            elements.append(Paragraph(f"- {flag}", body_style))
    else:
        elements.append(Paragraph("No significant risk flags identified.", body_style))
    elements.append(Spacer(1, 16))

    # AI Summary
    elements.append(Paragraph("AI Summary & Recommendation", heading_style))
    for line in ai_summary.split("\n"):
        if line.strip():
            elements.append(Paragraph(line, body_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.read()


def _make_table(data):
    table = Table(data, colWidths=[2.5 * inch, 2.5 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF1F8")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table
