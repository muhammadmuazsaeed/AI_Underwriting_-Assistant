"""
Quick script to view all saved analyses in a readable format.
Run this anytime with: python view_data.py
"""

import sqlite3

conn = sqlite3.connect("database/underwriting.db")
conn.row_factory = sqlite3.Row  # lets us access columns by name
cur = conn.cursor()

cur.execute("SELECT * FROM property_analyses ORDER BY id")
rows = cur.fetchall()

if not rows:
    print("No saved analyses yet.")
else:
    for row in rows:
        print("=" * 50)
        print(f"Analysis ID: {row['id']}  |  Saved on: {row['created_at']}")
        print("-" * 50)
        print(f"Purchase Price   : ${row['purchase_price']:,.0f}")
        print(f"Down Payment     : ${row['down_payment']:,.0f}")
        print(f"Monthly Rent     : ${row['monthly_rent']:,.0f}")
        print(f"Vacancy Rate     : {row['vacancy_rate']*100:.1f}%")
        print(f"NOI              : ${row['noi']:,.0f}")
        print(f"Cash Flow        : ${row['cash_flow']:,.0f}")
        print(f"Cap Rate         : {row['cap_rate']*100:.2f}%")
        print(f"ROI              : {row['roi']*100:.2f}%")
        print(f"Risk Level       : {row['risk_level']}")
        print(f"Risk Flags       : {row['risk_flags'] or 'None'}")
    print("=" * 50)

conn.close()