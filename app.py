"""KPI Dashboard -- Main entry point."""

import streamlit as st

from src.database import init_db
from src.authenticator import (
    ensure_admin_exists,
    login,
    get_current_user,
)

st.set_page_config(
    page_title="KPI Dashboard",
    page_icon="\U0001f4ca",
    layout="wide",
    initial_sidebar_state="expanded",
)

_CSS = (
    __import__("pathlib").Path(__file__).parent / "assets" / "style.css"
)
if _CSS.exists():
    st.markdown(
        f"<style>{_CSS.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )

init_db()
ensure_admin_exists()


# ── Login ────────────────────────────────────────────────────────────
def _login_page():
    st.markdown(
        '<div class="login-spacer"></div>',
        unsafe_allow_html=True,
    )
    _, center, _ = st.columns([1.2, 1, 1.2])
    with center:
        with st.container(border=True):
            st.markdown(
                """
                <div class="login-brand">
                    <div class="login-icon">\U0001f4ca</div>
                    <h1>KPI Dashboard</h1>
                    <p>Business intelligence for small companies</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.form("login_form"):
                email = st.text_input(
                    "Email", placeholder="admin@company.com"
                )
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button(
                    "Sign In",
                    use_container_width=True,
                    type="primary",
                )
            if submitted:
                if not email or not password:
                    st.error("Enter both email and password.")
                else:
                    ok, result = login(email, password)
                    if ok:
                        st.session_state["auth_token"] = result
                        st.rerun()
                    else:
                        st.error(result)
            st.caption("Default: admin@company.com / admin123")


# ── Dashboard ────────────────────────────────────────────────────────
def _dashboard(user):
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <span class="sidebar-logo">\U0001f4ca</span>
                <span class="sidebar-title">KPI Dashboard</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()
        st.markdown(f"**{user['email']}**")
        st.caption(f"Role: {user['role'].upper()}")
        st.divider()
        if st.button("\U0001f6aa Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.header("CEO Overview")
    st.caption("Business at a glance -- key metrics and trends.")

    k1, k2, k3, k4 = st.columns(4, gap="large")
    k1.metric("Total Revenue", "$92.0K", "+8.2%")
    k2.metric("Total Expenses", "$52.0K", "+4.1%")
    k3.metric("Net Cash Flow", "$40.0K", "+14.3%")
    k4.metric("Margin", "43.5%", "+1.2%")

    st.divider()
    st.info(
        "Upload real data to unlock full analytics. "
        "Views, KPI engine, and upload wizard coming soon."
    )


# ── Main ─────────────────────────────────────────────────────────────
def main():
    user = get_current_user()
    if not user:
        _login_page()
        return
    _dashboard(user)


main()
