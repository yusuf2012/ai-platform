from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine, Base
from routers import auth, ai
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Platform API",
    description="Full-stack AI app with chat, text analysis, and image analysis",
    version="1.0.0"
)

# CORS — allow the frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(ai.router)


@app.get("/health")
def health():
    return {"status": "ok", "message": "AI Platform is running"}


# Serve the frontend (index.html) for all non-API routes
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")

if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(os.path.join(frontend_path, "index.html"))
