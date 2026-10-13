from __future__ import annotations

import streamlit as st

from styles import inject_css
from views.auth_view import render_auth_view
from views.chat_view import render_chat_view

APP_NAME = "LinguaChat"


def main() -> None:
    """Entry point for the LinguaChat Streamlit application."""
    st.set_page_config(page_title=APP_NAME, page_icon="🌐", layout="wide", initial_sidebar_state="expanded")
    inject_css()
    st.session_state.setdefault("APP_NAME", APP_NAME)
    st.session_state.setdefault("token", None)
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("selected_user", None)

    if not st.session_state.get("token"):
        render_auth_view()
    else:
        render_chat_view()


if __name__ == "__main__":
    main()
