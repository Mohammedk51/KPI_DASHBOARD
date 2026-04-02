import pandas as pd
import plotly.express as px
import streamlit as st


def get_sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "revenue": [12000, 14000, 13500, 16000, 17500, 19000],
            "expenses": [7000, 8200, 7900, 9100, 9600, 10200],
        }
    )


def calculate_kpis(df: pd.DataFrame) -> dict:
    total_revenue = float(df["revenue"].sum())
    total_expenses = float(df["expenses"].sum())
    net_cash_flow = total_revenue - total_expenses
    margin_pct = (net_cash_flow / total_revenue * 100) if total_revenue else 0.0

    return {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_cash_flow": net_cash_flow,
        "margin_pct": margin_pct,
    }


def main() -> None:
    st.set_page_config(page_title="KPI Dashboard", layout="wide")
    st.title("Interactive Business KPI Dashboard (MVP)")
    st.caption("Simple Streamlit starter app with CI/CD-ready structure")

    df = get_sample_data()
    kpis = calculate_kpis(df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"${kpis['total_revenue']:,.0f}")
    c2.metric("Total Expenses", f"${kpis['total_expenses']:,.0f}")
    c3.metric("Net Cash Flow", f"${kpis['net_cash_flow']:,.0f}")
    c4.metric("Margin %", f"{kpis['margin_pct']:.1f}%")

    fig = px.line(df, x="month", y=["revenue", "expenses"], markers=True)
    fig.update_layout(title="Revenue vs Expenses Trend")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()
