"""
AI Underwriting Assistant -- Main Streamlit App
"""

import streamlit as st
from dotenv import load_dotenv

# IMPORTANT: load .env BEFORE importing chatbot.ai_chat,
# since that module reads the API key as soon as it's imported.
load_dotenv()

from calculations.noi import calculate_gross_income, calculate_operating_expenses, calculate_noi
from calculations.cashflow import calculate_cash_flow
from calculations.cap_rate import calculate_cap_rate
from calculations.roi import calculate_roi
from risk.risk_engine import assess_risk, RISK_COLORS
from visualization.charts import income_vs_expense_chart, cash_flow_chart, expense_breakdown_chart
from chatbot.context import build_context
from chatbot.ai_chat import ask_ai
from reports.report_generator import generate_pdf_report
from database.database import init_db, get_session
from database.models import PropertyAnalysis, ChatMessage
from ml_model import predict as ml_predict
from ml_model import trend_analysis as ml_trend

init_db()

st.set_page_config(page_title="AI Underwriting Assistant", layout="wide")
st.title("🏠 AI Underwriting Assistant")

# ---------------- Session state ----------------
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of {"role":..., "content":...}
if "saved_analysis_id" not in st.session_state:
    st.session_state.saved_analysis_id = None

# =========================================================================
# TOP ROW -- Property Details (left) + Market Insights (right, permanent)
# =========================================================================
top_left, top_right = st.columns([1, 1], gap="large")

with top_left:
    with st.container(border=True):
        st.subheader("🏠 Property Details")

        purchase_price = st.number_input("Purchase Price (PKR)", min_value=0.0, value=25000000.0, step=100000.0)
        down_payment = st.number_input("Down Payment (PKR)", min_value=0.0, value=5000000.0, step=100000.0)
        monthly_rent = st.number_input("Monthly Rent (PKR)", min_value=0.0, value=50000.0, step=1000.0)
        vacancy_rate_pct = st.slider("Vacancy Rate (%)", 0.0, 30.0, 5.0, step=0.5)

        st.markdown("**Annual Expenses**")
        property_tax = st.number_input("Property Tax (PKR/yr)", min_value=0.0, value=50000.0, step=5000.0)
        insurance = st.number_input("Insurance (PKR/yr)", min_value=0.0, value=25000.0, step=5000.0)
        maintenance = st.number_input("Maintenance (PKR/yr)", min_value=0.0, value=30000.0, step=5000.0)
        utilities = st.number_input("Utilities (PKR/yr)", min_value=0.0, value=0.0, step=5000.0)
        management_fee = st.number_input("Management Fee (PKR/yr)", min_value=0.0, value=36000.0, step=5000.0)
        other_expenses = st.number_input("Other Expenses (PKR/yr)", min_value=0.0, value=10000.0, step=5000.0)

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            analyze_clicked = st.button("🔍 Analyze Property", type="primary", use_container_width=True)
        with btn_col2:
            save_clicked = st.button("💾 Save Analysis", use_container_width=True)

with top_right:
    with st.container(border=True):
        st.subheader("📈 Market Insights (ML)")
        st.caption("Powered by a machine learning model trained on real Pakistan property market data (Zameen.com).")

        if not ml_predict.is_model_available():
            st.info(
                "Model not trained yet. Download the Zameen.com Pakistan dataset from Kaggle, "
                "save it as `data/zameen_data.csv`, then run `python -m ml_model.train_model` "
                "once to enable this section."
            )
        else:
            # This app is always used to check PURCHASE price (not rental listings),
            # so we fix "purpose" to "For Sale" -- no need to ask the user.
            purpose_choice = "For Sale"

            m1, m2 = st.columns(2)
            with m1:
                city_choice = st.selectbox("City", ml_predict.get_known_cities())
            with m2:
                property_type_choice = st.selectbox("Property Type", ml_predict.get_known_property_types())

            m3, m4 = st.columns(2)
            with m3:
                ml_bedrooms = st.number_input("Bedrooms", min_value=0, value=3, step=1, key="ml_bedrooms")
            with m4:
                ml_baths = st.number_input("Bathrooms", min_value=0, value=2, step=1, key="ml_baths")

            ml_area_marla = st.number_input("Area (in Marla)", min_value=0.0, value=10.0, step=0.5)
            location_choice = st.selectbox("Location (area/society)", ml_predict.get_known_locations())

            predict_clicked = st.button("🔮 Predict Market Price & Trend", use_container_width=True)

            if predict_clicked:
                with st.spinner("Running model..."):
                    predicted_price = ml_predict.predict_market_price(
                        city=city_choice,
                        location=location_choice,
                        property_type=property_type_choice,
                        purpose=purpose_choice,
                        bedrooms=ml_bedrooms,
                        baths=ml_baths,
                        area_marla=ml_area_marla,
                    )

                st.metric("Model's Estimated Market Price", f"PKR {predicted_price:,.0f}")

                # Compare against the purchase price entered on the left panel
                # (purchase_price is available directly since it's a live widget value)
                diff_pct = ((purchase_price - predicted_price) / predicted_price) * 100
                if diff_pct > 10:
                    st.warning(
                        f"⚠️ The entered purchase price is about {diff_pct:.1f}% "
                        f"**above** the model's estimated market price. This property may be overpriced."
                    )
                elif diff_pct < -10:
                    st.success(
                        f"✅ The entered purchase price is about {abs(diff_pct):.1f}% "
                        f"**below** the model's estimated market price. This could be a good deal."
                    )
                else:
                    st.info(
                        f"ℹ️ The entered purchase price is close to the model's estimated "
                        f"market price (within {abs(diff_pct):.1f}%). Looks fairly priced."
                    )

                # Historical trend for the chosen city/location
                try:
                    trend_summary = ml_trend.get_trend_summary(city_choice, location_choice)
                    if trend_summary["change_pct"] is not None:
                        st.write(
                            f"**Historical trend ({trend_summary['first_year']}–{trend_summary['last_year']}):** "
                            f"Average price per Marla **{trend_summary['direction']}** by "
                            f"{abs(trend_summary['change_pct']):.1f}% in this area, based on listing data available."
                        )
                        st.plotly_chart(
                            ml_trend.get_price_trend_chart(city_choice, location_choice),
                            use_container_width=True,
                        )
                    else:
                        st.write("Not enough historical data points for this specific location to show a trend.")
                except Exception:
                    st.write("Trend data unavailable for this selection.")

st.divider()

# ---------------- Run the analysis ----------------
if analyze_clicked:
    vacancy_rate = vacancy_rate_pct / 100

    gross_income = calculate_gross_income(monthly_rent, vacancy_rate)
    operating_expenses = calculate_operating_expenses(
        property_tax, insurance, maintenance, utilities, management_fee, other_expenses
    )
    noi = calculate_noi(gross_income, operating_expenses)
    cash_flow = calculate_cash_flow(noi, annual_debt_service=0)  # all-cash assumption for MVP
    cap_rate = calculate_cap_rate(noi, purchase_price)
    roi = calculate_roi(cash_flow, down_payment if down_payment > 0 else purchase_price)

    expense_ratio = operating_expenses / gross_income if gross_income > 0 else 1
    risk = assess_risk(vacancy_rate, roi, cap_rate, cash_flow, expense_ratio)

    inputs = {
        "purchase_price": purchase_price,
        "down_payment": down_payment,
        "monthly_rent": monthly_rent,
        "vacancy_rate": vacancy_rate,
        "property_tax": property_tax,
        "insurance": insurance,
        "maintenance": maintenance,
        "utilities": utilities,
        "management_fee": management_fee,
        "other_expenses": other_expenses,
    }
    metrics = {
        "gross_income": gross_income,
        "operating_expenses": operating_expenses,
        "noi": noi,
        "cash_flow": cash_flow,
        "cap_rate": cap_rate,
        "roi": roi,
    }

    st.session_state.inputs = inputs
    st.session_state.metrics = metrics
    st.session_state.risk = risk
    st.session_state.analysis_done = True
    st.session_state.chat_history = []  # reset chat for new analysis

# =========================================================================
# BELOW -- Results, Charts, Chatbot, PDF Report (only after Analyze)
# =========================================================================
if st.session_state.analysis_done:
    metrics = st.session_state.metrics
    risk = st.session_state.risk
    inputs = st.session_state.inputs

    st.header("Results")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("NOI", f"PKR {metrics['noi']:,.0f}")
    c2.metric("Cash Flow", f"PKR {metrics['cash_flow']:,.0f}")
    c3.metric("Cap Rate", f"{metrics['cap_rate']*100:.2f}%")
    c4.metric("ROI", f"{metrics['roi']*100:.2f}%")
    c5.metric("Risk", f"{RISK_COLORS[risk['level']]} {risk['level']}")

    if risk["flags"]:
        st.warning("**Risk flags:** " + "; ".join(risk["flags"]))

    st.plotly_chart(
        income_vs_expense_chart(metrics["gross_income"], metrics["operating_expenses"]),
        use_container_width=True,
    )
    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(cash_flow_chart(metrics["cash_flow"]), use_container_width=True)
    with col_b:
        expense_dict = {
            "Property Tax": inputs["property_tax"],
            "Insurance": inputs["insurance"],
            "Maintenance": inputs["maintenance"],
            "Utilities": inputs["utilities"],
            "Management Fee": inputs["management_fee"],
            "Other": inputs["other_expenses"],
        }
        st.plotly_chart(expense_breakdown_chart(expense_dict), use_container_width=True)

    # ---- Save to DB ----
    if save_clicked:
        session = get_session()
        record = PropertyAnalysis(
            purchase_price=inputs["purchase_price"],
            down_payment=inputs["down_payment"],
            monthly_rent=inputs["monthly_rent"],
            vacancy_rate=inputs["vacancy_rate"],
            property_tax=inputs["property_tax"],
            insurance=inputs["insurance"],
            maintenance=inputs["maintenance"],
            utilities=inputs["utilities"],
            management_fee=inputs["management_fee"],
            other_expenses=inputs["other_expenses"],
            noi=metrics["noi"],
            cash_flow=metrics["cash_flow"],
            cap_rate=metrics["cap_rate"],
            roi=metrics["roi"],
            risk_level=risk["level"],
            risk_flags=", ".join(risk["flags"]),
        )
        session.add(record)
        session.commit()
        st.session_state.saved_analysis_id = record.id
        session.close()
        st.success(f"Analysis saved (ID: {record.id})")

    # ---- AI Chatbot ----
    st.header("💬 Ask the AI Assistant")
    context = build_context(inputs, metrics, risk)

    # ---- Quick suggested questions (shown only before the first message) ----
    quick_question = None
    if not st.session_state.chat_history:
        st.caption("Quick questions — click one, or type your own below:")
        suggested_questions = [
            "Is this a good investment?",
            "Why is the cap rate low?",
            "Explain the risks.",
            "Summarize this analysis.",
        ]
        q_cols = st.columns(2)
        for i, q in enumerate(suggested_questions):
            if q_cols[i % 2].button(q, key=f"quick_q_{i}", use_container_width=True):
                quick_question = q

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_question = st.chat_input("Ask about this property...")
    final_question = quick_question or user_question

    if final_question:
        st.session_state.chat_history.append({"role": "user", "content": final_question})
        with st.chat_message("user"):
            st.write(final_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_ai(context, st.session_state.chat_history[:-1], final_question)
            st.write(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # ---- Generate Report ----
    st.header("📄 Investment Memo")
    if st.button("Generate PDF Report"):
        with st.spinner("Generating report..."):
            summary_prompt = "Generate an investment memo summarizing this property analysis."
            ai_summary = ask_ai(context, [], summary_prompt)
            pdf_bytes = generate_pdf_report(inputs, metrics, risk, ai_summary)
        st.download_button(
            "⬇️ Download PDF",
            data=pdf_bytes,
            file_name="investment_memo.pdf",
            mime="application/pdf",
        )

else:
    st.info("Fill in the property details above and click **Analyze Property** to see results, charts, and the AI chatbot.")
