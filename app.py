# app.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import os

# import json
from datetime import datetime
from typing import Dict, Optional
# import asyncio
# from pathlib import Path

# Import your existing modules
from services.download_transcript import get_youtube_transcript as transcript
from services.generate_manifest import (
    generate_manifest_from_transcript as generate_manifest,
)
from services.scaffold_project import scaffold


# app = FastAPI(title="YouTube Tutorial Scaffold API", version="1.0.0")
app = FastAPI(
    title="YouTube Tutorial Scaffold API",
    version="1.0.0",
    docs_url=None,  # Disable Swagger UI
    redoc_url=None,  # Disable ReDoc
    openapi_url=None,  # Disable OpenAPI schema endpoint
)
# Add CORS middleware for frontend access

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://y2-p.vercel.app",
        "https://y2-p.vercel.app/",  # With trailing slash
        # "http://localhost:3000",  # For local development (optional)
        # "http://127.0.0.1:3000",  # For local development (optional)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],  # Only allow specific methods
    allow_headers=["*"],
)

# In-memory task storage (in production, use Redis or database)
tasks: Dict[str, Dict] = {}


class VideoRequest(BaseModel):
    url: str


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str


class TaskStatus(BaseModel):
    task_id: str
    status: str
    message: str
    created_at: str
    completed_at: Optional[str] = None
    download_url: Optional[str] = None
    error: Optional[str] = None


def update_task_status(
    task_id: str, status: str, message: str, error: str = None, download_url: str = None
):
    """Update task status in storage"""
    if task_id in tasks:
        tasks[task_id].update(
            {
                "status": status,
                "message": message,
                "error": error,
                "download_url": download_url,
            }
        )
        if status in ["completed", "failed"]:
            tasks[task_id]["completed_at"] = datetime.now().isoformat()


async def process_video_task(task_id: str, video_url: str):
    """Background task to process video"""
    try:
        # Update status to processing
        update_task_status(task_id, "processing", "Downloading transcript...")

        # Step 1: Get transcript
        transcription = transcript(video_url)
        if not transcription:
            raise Exception("Failed to get transcription")

        update_task_status(task_id, "processing", "Generating project manifest...")

        # Step 2: Generate manifest
        manifest = generate_manifest()
        if not manifest:
            raise Exception("Failed to generate manifest")

        update_task_status(task_id, "processing", "Creating project files...")

        # Step 3: Create project scaffold
        scaffold(manifest=manifest, task_id=task_id)

        # Update status to completed
        download_url = f"/download/{task_id}"
        update_task_status(
            task_id,
            "completed",
            "Project scaffold created successfully",
            download_url=download_url,
        )

    except Exception as e:
        # Update status to failed
        update_task_status(task_id, "failed", "Failed to process video", error=str(e))


@app.post("/process", response_model=TaskResponse)
async def process_video(request: VideoRequest, background_tasks: BackgroundTasks):
    """
    Submit a YouTube video for processing
    Returns a task ID to track progress
    """
    # Generate unique task ID
    task_id = str(uuid.uuid4())

    # Initialize task in storage
    tasks[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "message": "Task queued for processing",
        "created_at": datetime.now().isoformat(),
        "video_url": request.url,
        "completed_at": None,
        "download_url": None,
        "error": None,
    }

    # Add background task
    background_tasks.add_task(process_video_task, task_id, request.url)

    return TaskResponse(
        task_id=task_id,
        status="pending",
        message="Video processing started. Use /status/{task_id} to check progress.",
    )


@app.get("/status/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """
    Get the status of a processing task
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasks[task_id]
    return TaskStatus(**task)


@app.get("/download/{task_id}")
async def download_project(task_id: str):
    """
    Download the generated project zip file
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasks[task_id]

    if task["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Project not ready. Current status: {task['status']}",
        )

    # FIXED: Find the zip file in /tmp
    zip_path = f"/tmp/{task_id}_project.zip"

    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="Project file not found")

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"youtube_project_{task_id}.zip",
    )


@app.get("/tasks")
async def list_all_tasks():
    """
    List all tasks (for debugging/admin purposes)
    """
    return {"tasks": list(tasks.values())}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """
    Delete a task and its associated files
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    # FIXED: Remove files from /tmp
    zip_path = f"/tmp/{task_id}_project.zip"
    project_dir = f"/tmp/{task_id}_project"

    try:
        if os.path.exists(zip_path):
            os.remove(zip_path)
        if os.path.exists(project_dir):
            import shutil

            shutil.rmtree(project_dir)
    except Exception as e:
        print(f"Error cleaning up files: {e}")

    # Remove from tasks
    del tasks[task_id]

    return {"message": "Task deleted successfully"}


#################################################


# Update your root endpoint to include request count
@app.get("/")
async def root():
    """
    API health check and documentation
    """
    return {
        "message": "YouTube Tutorial Scaffold API",
        "version": "1.0.0",
        "endpoints": {
            "POST /process": "Submit video for processing",
            "GET /status/{task_id}": "Check task status",
            "GET /download/{task_id}": "Download completed project",
            "GET /tasks": "List all tasks",
            "DELETE /tasks/{task_id}": "Delete task and files",
        },
        "usage": {
            "1": "POST your YouTube URL to /process",
            "2": "Get task_id in response",
            "3": "Check status with GET /status/{task_id}",
            "4": "When status is 'completed', download with GET /download/{task_id}",
        },
    }


# FIXED: Update the main section
if __name__ == "__main__":
    import uvicorn

    # Create tmp directory if it doesn't exist (though it should)
    os.makedirs("/tmp", exist_ok=True)

    uvicorn.run(app, host="0.0.0.0", port=8000)
