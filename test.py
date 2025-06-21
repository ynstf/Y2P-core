#!/usr/bin/env python3
"""
Example client for the YouTube Tutorial Scaffold API
Shows how to submit a video, track progress, and download the result
"""

import requests
import time

API_BASE = "http://localhost:8000"


def submit_video(url: str) -> str:
    """Submit a video for processing"""
    response = requests.post(f"{API_BASE}/process", json={"url": url})

    if response.status_code == 200:
        data = response.json()
        print("✅ Video submitted successfully!")
        print(f"📋 Task ID: {data['task_id']}")
        print(f"📝 Status: {data['status']}")
        return data["task_id"]
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return None


def check_status(task_id: str) -> dict:
    """Check the status of a task"""
    response = requests.get(f"{API_BASE}/status/{task_id}")

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error checking status: {response.status_code} - {response.text}")
        return None


def download_project(task_id: str, filename: str = None) -> bool:
    """Download the completed project"""
    if not filename:
        filename = f"project_{task_id}.zip"

    response = requests.get(f"{API_BASE}/download/{task_id}")

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Project downloaded as {filename}")
        return True
    else:
        print(f"❌ Error downloading: {response.status_code} - {response.text}")
        return False


def main():
    """Main example workflow"""
    print("🎥 YouTube Tutorial Scaffold API Client")
    print("=" * 40)

    # Example URL (replace with actual tutorial URL)
    video_url = input("Enter YouTube URL: ").strip()

    if not video_url:
        video_url = "https://youtu.be/nF_crEtmpBo"
        print(f"Using example URL: {video_url}")

    # Step 1: Submit video
    task_id = submit_video(video_url)
    if not task_id:
        return

    print("\n🔄 Monitoring task progress...")
    print("-" * 30)

    # Step 2: Monitor progress
    while True:
        status_data = check_status(task_id)
        if not status_data:
            break

        status = status_data["status"]
        message = status_data["message"]

        print(f"📊 Status: {status.upper()}")
        print(f"💬 Message: {message}")

        if status == "completed":
            print("✅ Processing completed!")
            if status_data.get("download_url"):
                print(f"🔗 Download URL: {API_BASE}{status_data['download_url']}")

            # Step 3: Download the project
            print("\n📥 Downloading project...")
            if download_project(task_id):
                print("🎉 Success! Your project is ready.")
            break

        elif status == "failed":
            print("❌ Processing failed!")
            if status_data.get("error"):
                print("🚨 Error: {status_data['error']}")
            break

        elif status in ["pending", "processing"]:
            print("⏳ Still working... (waiting 5 seconds)")
            time.sleep(5)

        print("-" * 30)


def list_tasks():
    """List all tasks (for debugging)"""
    response = requests.get(f"{API_BASE}/tasks")
    if response.status_code == 200:
        tasks = response.json()["tasks"]
        print(f"📋 Found {len(tasks)} tasks:")
        for task in tasks:
            print(f"  - {task['task_id']}: {task['status']} ({task['created_at']})")
    else:
        print(f"❌ Error: {response.text}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_tasks()
    else:
        main()
