# AI Platform

A full-stack web application with user authentication and three AI-powered tools built with FastAPI and Gemini AI.

## Features

- **User authentication** — register, login, JWT tokens, protected routes
- **AI Chat** — conversational AI assistant with memory within a session
- **Text Analysis** — summarise, sentiment analysis, key point extraction
- **Image Analysis** — upload any image and ask questions about it

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, SQLAlchemy, SQLite |
| Auth | JWT tokens, bcrypt password hashing |
| AI | Google Gemini API |
| Frontend | Vanilla HTML/CSS/JS (no framework needed) |

## Setup

### 1. Clone and open in VS Code
```bash
cd ai-platform
code .
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Edit `backend/.env`:
```
GEMINI_API_KEY=your_key_here
SECRET_KEY=any-long-random-string
```

Get a free Gemini API key at: https://aistudio.google.com

### 5. Run the server
```bash
cd backend
uvicorn main:app --reload
```

### 6. Open the app
Open `frontend/index.html` in your browser, or visit:
- App: http://localhost:8000
- API docs: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/auth/register | Create account |
| POST | /api/auth/login | Login |
| GET | /api/auth/me | Get current user |
| POST | /api/ai/chat | Chat with AI |
| POST | /api/ai/analyse-text | Analyse text |
| POST | /api/ai/analyse-image | Analyse image |
| GET | /health | Health check |
