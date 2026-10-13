from __future__ import annotations

import streamlit as st

from api_client import ApiError, get_languages, login, signup


@st.cache_data(ttl=3600)
def get_languages_cached() -> list[dict[str, str]]:
    """Return the supported language list with a safe English fallback."""
    try:
        return get_languages()
    except ApiError:
        return [{"code": "en", "name": "English"}]


def render_auth_view() -> None:
    """Render the sign-in and sign-up experience."""
    left, center, right = st.columns([1, 1.2, 1])
    with center:
        st.markdown('<div class="auth-shell">', unsafe_allow_html=True)
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown(
            f'<p class="brand-title">{st.session_state.get("APP_NAME", "LinguaChat")} 🌐</p>',
            unsafe_allow_html=True,
        )
        st.markdown('<p class="brand-subtitle">Talk to anyone, in any language.</p>', unsafe_allow_html=True)

        login_tab, signup_tab = st.tabs(["Log in", "Sign up"])

        with login_tab:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Log in", use_container_width=True)
                if submitted:
                    if not username.strip() or not password.strip():
                        st.error("Username and password are required.")
                    else:
                        with st.spinner("Signing in..."):
                            try:
                                response = login(username.strip(), password)
                            except ApiError as exc:
                                st.error(exc.message)
                            else:
                                st.session_state.token = response["access_token"]
                                st.session_state.user = response["user"]
                                st.session_state.selected_user = None
                                st.rerun()

        with signup_tab:
            with st.form("signup_form"):
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm password", type="password")
                languages = get_languages_cached()
                language_codes = [item["code"] for item in languages]
                default_index = language_codes.index("en") if "en" in language_codes else 0
                preferred_language = st.selectbox(
                    "Your preferred language",
                    options=language_codes,
                    format_func=lambda code: next(item["name"] for item in languages if item["code"] == code),
                    index=default_index,
                )
                st.caption("At least 8 characters with a letter and a number")
                submitted = st.form_submit_button("Create account", use_container_width=True)
                if submitted:
                    if not username.strip() or not email.strip() or not password or not confirm_password:
                        st.error("Please complete all sign-up fields.")
                    elif password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        with st.spinner("Creating your account..."):
                            try:
                                response = signup(
                                    username.strip(),
                                    email.strip(),
                                    password,
                                    preferred_language,
                                )
                            except ApiError as exc:
                                st.error(exc.message)
                            else:
                                st.session_state.token = response["access_token"]
                                st.session_state.user = response["user"]
                                st.session_state.selected_user = None
                                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
