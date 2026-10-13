from __future__ import annotations

import html
from datetime import datetime

import streamlit as st

from api_client import ApiError, get_messages, list_users, send_text_message, update_language


@st.cache_data(ttl=3600)
def get_language_options() -> list[dict[str, str]]:
    """Fetch language names once per hour for the sidebar selectors."""
    try:
        from api_client import get_languages

        return get_languages()
    except ApiError:
        return [{"code": "en", "name": "English"}]


def get_language_name(code: str | None) -> str:
    """Resolve a language code to a display name."""
    if not code:
        return "Unknown"
    for language in get_language_options():
        if language["code"] == code:
            return language["name"]
    return code


def build_message_html(messages: list[dict[str, object]], current_user_id: int) -> str:
    """Build the HTML for the message list with safe escaping and timestamps."""
    parts: list[str] = ["<div class='chat-window'><div class='chat-inner'>"]
    if not messages:
        parts.append("<div class='empty-chat'><div><span class='emoji'>💬</span><div>No messages yet. Say hello 👋</div></div></div>")
        parts.append("</div></div>")
        return "".join(parts)

    for message in messages:
        sender_id = int(message["sender_id"])
        row_class = "sent" if sender_id == current_user_id else "received"
        display_text = message.get("translated_text") if row_class == "received" and message.get("translated_text") is not None else message["original_text"]
        safe_text = html.escape(str(display_text)).replace("\n", "<br>")
        created_at = str(message["created_at"])
        if created_at.endswith("Z"):
            created_at = created_at.replace("Z", "+00:00")
        # This uses the server's local timezone when the backend emits offset-aware timestamps.
        timestamp = datetime.fromisoformat(created_at).astimezone().strftime("%H:%M")

        original_text = ""
        if row_class == "received" and message.get("translated_text") is not None and str(message["translated_text"]) != str(message["original_text"]):
            original_text = (
                "<div class='msg-original'>Original: "
                f"{html.escape(str(message['original_text']))}</div>"
            )

        parts.append(
            f"<div class='msg-row {row_class}'><div class='bubble'>{safe_text}</div>{original_text}<div class='msg-time'>{timestamp}</div></div>"
        )

    parts.append("</div></div>")
    return "".join(parts)


def render_sidebar(token: str, user: dict[str, object]) -> None:
    """Render the user list and profile settings in the sidebar."""
    with st.sidebar:
        user_name = str(user.get("username", "User"))
        user_language = get_language_name(str(user.get("preferred_language", "en")))
        st.markdown(
            f"""
            <div class="profile-card">
                <div class="profile-avatar">{user_name[0].upper()}</div>
                <div class="profile-meta">
                    <div class="profile-name">{html.escape(user_name)}</div>
                    <div class="profile-language">{html.escape(user_language)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        languages = get_language_options()
        language_codes = [item["code"] for item in languages]
        current_language = str(user.get("preferred_language", "en"))
        selected_language = st.selectbox(
            "My language",
            options=language_codes,
            format_func=lambda code: next(item["name"] for item in languages if item["code"] == code),
            index=language_codes.index(current_language) if current_language in language_codes else 0,
            key="my_language_select",
        )
        if selected_language != current_language:
            try:
                updated = update_language(token, selected_language)
            except ApiError as exc:
                st.error(exc.message)
            else:
                st.session_state.user = updated
                st.toast("Language updated")

        st.text_input("Search people", placeholder="Search by username", key="people_search")

        search_term = str(st.session_state.get("people_search", "")).strip()
        try:
            users = list_users(token, search=search_term)
        except ApiError as exc:
            st.warning(exc.message)
            users = []

        if users:
            for user_item in users:
                selected = bool(st.session_state.get("selected_user") and st.session_state.selected_user.get("id") == user_item["id"])
                label = f"{'● ' if selected else ''}{user_item['username']} · {get_language_name(user_item.get('preferred_language', 'en'))}"
                if st.button(label, type="primary" if selected else "secondary", key=f"user_{user_item['id']}"):
                    st.session_state.selected_user = user_item
        else:
            st.caption("No users found. Ask a friend to sign up!")

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        if st.button("Log out"):
            for key in ("token", "user", "selected_user"):
                st.session_state.pop(key, None)
            st.rerun()


def render_chat_header(partner: dict[str, object]) -> None:
    """Render the chat header with the selected user's details."""
    partner_name = str(partner.get("username", "User"))
    partner_language = get_language_name(str(partner.get("preferred_language", "en")))
    st.markdown(
        f"""
        <div class="chat-header">
            <div class="chat-avatar">{partner_name[0].upper()}</div>
            <div>
                <div class="chat-name">{html.escape(partner_name)}</div>
                <div class="chat-language">{html.escape(partner_language)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.fragment(run_every=3)
def message_list_fragment(token: str, current_user_id: int, partner_id: int) -> None:
    """Refresh the conversation list at regular intervals and render it as HTML."""
    try:
        messages = get_messages(token, partner_id, limit=200)
    except ApiError as exc:
        if exc.status_code == 401:
            for key in ("token", "user", "selected_user"):
                st.session_state.pop(key, None)
            st.rerun()
        else:
            st.warning(exc.message)
        return

    html_content = build_message_html(messages, current_user_id)
    st.markdown(html_content, unsafe_allow_html=True)


def render_input(token: str, partner_id: int) -> None:
    """Render the chat input form outside the polling fragment."""
    message = st.chat_input("Type a message...")
    if message is not None and message.strip():
        try:
            send_text_message(token, partner_id, message.strip())
        except ApiError as exc:
            st.error(exc.message)
        else:
            st.rerun()


def render_chat_view() -> None:
    """Render the authenticated chat interface."""
    token = st.session_state.get("token")
    user = st.session_state.get("user")
    if not token or not user:
        return

    render_sidebar(token, user)
    partner = st.session_state.get("selected_user")

    if partner is None:
        st.markdown(
            '<div class="empty-state"><div><span class="emoji">💬</span><div>Select someone from the sidebar to start chatting</div></div></div>',
            unsafe_allow_html=True,
        )
        return

    render_chat_header(partner)
    message_list_fragment(token, int(user["id"]), int(partner["id"]))
    render_input(token, int(partner["id"]))
