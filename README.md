# AI-Powered Cross-Language Messaging System

This project is a backend-first messaging platform that lets users register, choose a preferred language, and exchange text and voice messages that are translated automatically for the recipient. The system is built with Python, FastAPI, SQLite, and later integrates translation and speech processing services.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python, FastAPI |
| Database | SQLite, SQLAlchemy |
| Authentication | JWT, bcrypt |
| Configuration | Pydantic Settings |
| Frontend (later) | Streamlit |
| Speech / Translation (later) | Groq Whisper, Google Gemini |

## Planned Phases

- [x] Phase 1: Backend foundation and authentication
- [ ] Phase 2: Streamlit frontend and user flows
- [ ] Phase 3: Translation services and message handling
- [ ] Phase 4: Voice notes, speech-to-text, and text-to-speech

## Local Setup

1. Open a terminal in the project root.
2. Navigate to the backend folder:
   ```bash
   cd backend
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
4. Activate it:
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - Windows PowerShell:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
5. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
6. Copy the sample environment file and create your local configuration:
   ```bash
   cp .env.example .env
   ```
7. Generate a `SECRET_KEY` and update `.env`:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
8. Start the backend server from inside the `backend` folder:
   ```bash
   uvicorn app.main:app --reload
   ```
9. Open the API docs in your browser at:
   ```text
   http://127.0.0.1:8000/docs
   ```
