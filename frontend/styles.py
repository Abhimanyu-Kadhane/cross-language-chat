from __future__ import annotations

import streamlit as st


def inject_css() -> None:
    """Inject the custom UI styling for the chat application."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: "Inter", sans-serif;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {background: transparent;}

        .block-container {
            padding-top: 1rem;
        }

        .auth-shell {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 90vh;
        }

        .auth-card {
            width: 100%;
            max-width: 440px;
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 16px 40px rgba(23, 24, 33, 0.08);
            padding: 2rem 1.5rem;
            margin: 0 auto;
        }

        .brand-title {
            margin: 0;
            font-size: 2.35rem;
            font-weight: 800;
            letter-spacing: -0.05em;
            background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .brand-subtitle {
            margin: 0.35rem 0 1.2rem;
            color: #5b6477;
            font-size: 0.98rem;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #ebedf8;
        }

        .sidebar-section {
            margin-bottom: 1rem;
        }

        .profile-card {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            background: linear-gradient(135deg, #f6f3ff 0%, #eef2ff 100%);
            border: 1px solid #ebebff;
            border-radius: 14px;
            padding: 0.85rem 0.8rem;
            margin: 0.1rem 0 0.8rem;
        }

        .profile-avatar {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: linear-gradient(135deg, #5b5bd6 0%, #7c3aed 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1rem;
            flex-shrink: 0;
        }

        .profile-meta {
            display: flex;
            flex-direction: column;
            min-width: 0;
        }

        .profile-name {
            font-weight: 700;
            color: #1f2430;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .profile-language {
            font-size: 0.72rem;
            color: #687387;
        }

        div[data-testid="stVerticalBlock"] .stButton > button {
            width: 100%;
            display: flex;
            justify-content: flex-start;
            align-items: center;
            background: #ffffff;
            color: #1f2430;
            border: 1px solid #e9ecf6;
            border-radius: 12px;
            padding: 0.7rem 0.8rem;
            margin-bottom: 0.4rem;
            box-shadow: none;
            transition: all 0.2s ease;
        }

        div[data-testid="stVerticalBlock"] .stButton > button:hover {
            border-color: #dfe5ff;
            background: #f7f7ff;
        }

        div[data-testid="stVerticalBlock"] .stButton > button[kind="primary"] {
            background: #eef0ff;
            border-color: #dfe2ff;
            color: #2b2fc3;
        }

        .chat-window {
            display: flex;
            flex-direction: column-reverse;
            height: 62vh;
            overflow-y: auto;
            background: #ffffff;
            border: 1px solid #ececf7;
            border-radius: 16px;
            padding: 0.8rem;
            scrollbar-width: thin;
        }

        .chat-inner {
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 100%;
        }

        .msg-row {
            display: flex;
            flex-direction: column;
            width: 100%;
        }

        .msg-row.sent {
            align-items: flex-end;
        }

        .msg-row.received {
            align-items: flex-start;
        }

        .bubble {
            max-width: 70%;
            padding: 10px 14px;
            border-radius: 18px;
            word-wrap: break-word;
            white-space: pre-wrap;
            line-height: 1.45;
        }

        .msg-row.sent .bubble {
            background: linear-gradient(135deg, #5b5bd6 0%, #7c3aed 100%);
            color: #ffffff;
            border-bottom-right-radius: 6px;
        }

        .msg-row.received .bubble {
            background: #ffffff;
            border: 1px solid #ebedf5;
            color: #1f2430;
            border-bottom-left-radius: 6px;
        }

        .msg-time {
            margin-top: 4px;
            font-size: 0.67rem;
            color: #7a8194;
        }

        .msg-row.sent .msg-time {
            text-align: right;
            margin-right: 4px;
        }

        .msg-row.received .msg-time {
            text-align: left;
            margin-left: 4px;
        }

        .msg-original {
            margin-top: 4px;
            font-size: 0.7rem;
            color: #7a8194;
            font-style: italic;
        }

        .msg-row.sent .msg-original {
            display: none;
        }

        .empty-state,
        .empty-chat {
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #66708a;
            min-height: 180px;
            font-size: 1rem;
            padding: 1rem;
        }

        .empty-state {
            min-height: 60vh;
        }

        .empty-state .emoji,
        .empty-chat .emoji {
            display: block;
            font-size: 2.2rem;
            margin-bottom: 0.35rem;
        }

        .chat-header {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            padding: 0.85rem 0.25rem 1rem;
            border-bottom: 1px solid #eef1f8;
            margin-bottom: 0.8rem;
        }

        .chat-avatar {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: linear-gradient(135deg, #e0e5ff 0%, #ede7ff 100%);
            color: #3a3e92;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
        }

        .chat-name {
            font-weight: 700;
            color: #1f2430;
        }

        .chat-language {
            font-size: 0.72rem;
            color: #737d90;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
