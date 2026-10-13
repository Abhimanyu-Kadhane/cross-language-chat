from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st

REQUEST_TIMEOUT = 60


class ApiError(Exception):
    """Raised when the backend request fails with a friendly user-facing message."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def get_backend_url() -> str:
    """Return the backend base URL without a trailing slash."""
    try:
        value = st.secrets["BACKEND_URL"]
    except Exception:
        value = os.getenv("BACKEND_URL")

    if not value:
        value = "http://127.0.0.1:8000"
    return str(value).rstrip("/")


def _request(method: str, path: str, token: str | None = None, **kwargs: Any) -> Any:
    """Send a request using the configured backend URL and normalize backend errors."""
    url = f"{get_backend_url()}{path}"
    headers = dict(kwargs.pop("headers", {}))
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.request(method, url, timeout=REQUEST_TIMEOUT, headers=headers, **kwargs)
    except (requests.ConnectionError, requests.Timeout):
        raise ApiError("Cannot reach the server. Please check that the backend is running.", None) from None

    try:
        payload = response.json()
    except ValueError:
        payload = {}

    if 200 <= response.status_code < 300:
        return payload

    detail = payload.get("detail") if isinstance(payload, dict) else None
    if isinstance(detail, list):
        messages: list[str] = []
        for item in detail:
            if isinstance(item, dict):
                msg = item.get("msg")
                if msg:
                    messages.append(str(msg))
            elif isinstance(item, str):
                messages.append(item)
        if messages:
            message = " ".join(messages)
            message = message.replace("Value error, ", "", 1)
        else:
            message = "The request was invalid."
    elif isinstance(detail, str):
        message = detail
    else:
        message = "Something went wrong. Please try again."

    raise ApiError(message, response.status_code)


def signup(username: str, email: str, password: str, preferred_language: str) -> dict[str, Any]:
    """Create a user account and return the auth payload."""
    return _request(
        "POST",
        "/auth/signup",
        json={
            "username": username,
            "email": email,
            "password": password,
            "preferred_language": preferred_language,
        },
    )


def login(username: str, password: str) -> dict[str, Any]:
    """Authenticate a user and return the auth payload."""
    return _request("POST", "/auth/login", json={"username": username, "password": password})


def get_me(token: str) -> dict[str, Any]:
    """Fetch the authenticated user profile."""
    return _request("GET", "/users/me", token=token)


def update_language(token: str, preferred_language: str) -> dict[str, Any]:
    """Update the authenticated user's preferred language."""
    return _request(
        "PATCH",
        "/users/me/language",
        token=token,
        json={"preferred_language": preferred_language},
    )


def get_languages() -> list[dict[str, str]]:
    """Fetch the list of supported languages from the backend."""
    return _request("GET", "/languages")


def list_users(token: str, search: str = "") -> list[dict[str, Any]]:
    """List users that are available for chat."""
    params = {"search": search} if search else {}
    return _request("GET", "/users", token=token, params=params)


def send_text_message(token: str, receiver_id: int, text: str) -> dict[str, Any]:
    """Send a text message to another user."""
    return _request(
        "POST",
        "/messages/text",
        token=token,
        json={"receiver_id": receiver_id, "text": text},
    )


def get_messages(token: str, other_user_id: int, limit: int = 200) -> list[dict[str, Any]]:
    """Fetch the conversation between the current user and another user."""
    return _request("GET", f"/messages/{other_user_id}", token=token, params={"limit": limit})
