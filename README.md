# YouTube Tutorial to Project Scaffold

An automated tool that watches programming tutorial videos and generates complete, runnable project scaffolds from them. Simply provide a YouTube URL, and the system will extract the transcript, analyze the code structure, and create a fully organized project directory with all files and folders.

## Features

- **Automatic Transcript Extraction**: Downloads video transcripts from YouTube tutorials
- **AI-Powered Code Analysis**: Uses Google Gemini AI to parse transcripts and identify project structure
- **Complete Project Generation**: Creates folders, files, and organizes code exactly as shown in tutorials
- **Ready-to-Run Output**: Generates a zipped project folder ready for immediate use
- **Smart Error Handling**: Handles common parsing issues and file format corrections
- **FastAPI Web Interface**: Modern REST API for easy integration and web-based usage
- **Asynchronous Processing**: Background task processing with real-time status tracking
- **File Downloads**: Direct download links for completed projects

## Prerequisites

- Python 3.7+
- Google Gemini API key
- Internet connection for transcript fetching

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ynstf/Y2P-core
   cd Y2P-core
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env-template .env
   ```
   Edit `.env` and add your Google Gemini API key:
   ```
   GEMINI_API_KEY = "your-actual-api-key-here"
   ```

4. **Create output directory**
   ```bash
   mkdir output
   ```

## Usage

### Option 1: FastAPI Web Server (Recommended)

Start the FastAPI server:

```bash
python app.py
```

The server will start on `http://localhost:8000`. You can:

- **View API documentation**: Visit `http://localhost:8000/docs` for interactive Swagger docs
- **Use the REST API**: Submit videos and track progress programmatically
- **Access the root endpoint**: `http://localhost:8000/` for API information

#### API Endpoints

- `POST /process` - Submit a YouTube video for processing
- `GET /status/{task_id}` - Check processing status
- `GET /download/{task_id}` - Download completed project
- `GET /tasks` - List all tasks (admin/debug)
- `DELETE /tasks/{task_id}` - Delete task and cleanup files

#### Example API Usage

```python
import requests

# Submit video for processing
response = requests.post("http://localhost:8000/process", 
                        json={"url": "https://youtube.com/watch?v=VIDEO_ID"})
task_data = response.json()
task_id = task_data["task_id"]

# Check status
status_response = requests.get(f"http://localhost:8000/status/{task_id}")
status = status_response.json()

# Download when completed
if status["status"] == "completed":
    download_response = requests.get(f"http://localhost:8000/download/{task_id}")
    with open("project.zip", "wb") as f:
        f.write(download_response.content)
```

#### Using the Test Client

A complete example client is provided in `test.py`:

```bash
python test.py
```

This will guide you through the entire process: submitting a video, monitoring progress, and downloading the result.

### Option 2: Command Line Interface

Run the main script and provide a YouTube tutorial URL when prompted:

```bash
python main.py
```

The system will:
1. Extract the video transcript
2. Generate a project manifest using AI
3. Create the complete project structure
4. Package everything in a zip file

### Example Workflow

**Command Line:**
```bash
$ python main.py
put video URL : https://www.youtube.com/watch?v=nF_crEtmpBo
transcription ok: [transcript content]
manifest ok: {'folders': [...], 'files': {...}}
Project scaffolded and zipped as output\final_project.zip
```

**API Workflow:**
```bash
$ python test.py
Enter YouTube URL: https://www.youtube.com/watch?v=nF_crEtmpBo
✅ Video submitted successfully!
📋 Task ID: abc123-def456-ghi789
📊 Status: PROCESSING
💬 Message: Downloading transcript...
⏳ Still working... (waiting 5 seconds)
📊 Status: COMPLETED
✅ Processing completed!
📥 Downloading project...
✅ Project downloaded as project_abc123-def456-ghi789.zip
🎉 Success! Your project is ready.
```

### Advanced Usage

You can also use individual components programmatically:

```python
from services.download_transcript import get_youtube_transcript
from services.generate_manifest import generate_manifest_from_transcript
from services.scaffold_project import scaffold

# Get transcript
transcript = get_youtube_transcript("https://youtube.com/watch?v=VIDEO_ID")

# Generate manifest
manifest = generate_manifest_from_transcript()

# Create project
scaffold(manifest, task_id="custom_id")
```

## Project Structure

```
youtube-tutorial-scaffold/
├── app.py                      # FastAPI web server
├── main.py                     # Command line entry point
├── test.py                     # Example API client
├── services/                   # Core processing modules
│   ├── __init__.py
│   ├── download_transcript.py  # YouTube transcript extraction
│   ├── generate_manifest.py    # AI-powered manifest generation
│   └── scaffold_project.py     # Project file/folder creation
├── requirements.txt            # Python dependencies
├── .env-template              # Environment variables template
├── urls.txt                   # Sample URLs for testing
└── output/                    # Generated files directory
    ├── transcript.txt         # Raw video transcript
    ├── manifest.json          # Structured project manifest
    ├── {task_id}_project/     # Generated project files
    └── {task_id}_project.zip  # Zipped project
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### FastAPI Configuration

The FastAPI server runs on:
- **Host**: `0.0.0.0` (accessible from all interfaces)
- **Port**: `8000`
- **CORS**: Enabled for all origins (configure for production)

### Customization

You can modify the AI prompt in `services/generate_manifest.py` to:
- Change the output format
- Add specific file type handling
- Adjust parsing accuracy
- Include additional metadata

## Output Format

The system generates a JSON manifest with this structure:

```json
{
  "folders": [
    "relative/path/to/folder",
    "another/folder"
  ],
  "files": {
    "main.py": "# Complete file contents here",
    "config.json": "{ \"setting\": \"value\" }",
    "subfolder/utils.py": "# More code here"
  }
}
```

## Supported Video Types

Works best with:
- **Coding tutorials** with clear step-by-step file creation
- **Project walkthroughs** showing complete implementations
- **Course content** with structured programming lessons

May struggle with:
- Videos without clear code structure
- Live coding sessions with lots of backtracking
- Tutorials mixing multiple unrelated projects

## API Response Formats

### Task Status Response
```json
{
  "task_id": "abc123-def456-ghi789",
  "status": "completed",
  "message": "Project scaffold created successfully",
  "created_at": "2024-01-15T10:30:00",
  "completed_at": "2024-01-15T10:32:30",
  "download_url": "/download/abc123-def456-ghi789",
  "error": null
}
```

### Status Values
- `pending` - Task queued for processing
- `processing` - Currently being processed
- `completed` - Successfully completed
- `failed` - Processing failed

## Troubleshooting

### Common Issues

**"Request failed with status"**
- Check your internet connection
- Verify the YouTube URL is accessible
- Some videos may have transcript restrictions

**"Failed to parse JSON"**
- The AI might have generated malformed output
- Check the raw response in the error message
- Try with a different tutorial video

**"No such file or directory"**
- Ensure the `output` directory exists
- Check file permissions
- Verify the transcript was downloaded successfully

**"Task not found" (API)**
- Check if the task_id is correct
- Tasks are stored in memory and cleared on server restart
- Use `GET /tasks` to list all available tasks

### Debug Mode

For the FastAPI server, check the console output for detailed processing steps. For the CLI version, enable verbose output by modifying the print statements in each module.

### Development

To run the FastAPI server in development mode with auto-reload:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

For production deployment:

1. **Use a production ASGI server** like Gunicorn with Uvicorn workers
2. **Configure CORS** to restrict origins to your frontend domain
3. **Use a persistent task store** (Redis, database) instead of in-memory storage
4. **Add authentication** and rate limiting
5. **Set up reverse proxy** (Nginx) for static files and load balancing
6. **Configure environment variables** securely

Example production command:
```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes. Always respect:
- YouTube's Terms of Service
- Video creators' intellectual property rights
- API rate limits and usage policies

## Acknowledgments

- NoteGPT API for transcript extraction
- Google Gemini for AI-powered code analysis
- FastAPI for the modern web framework
- The programming tutorial community for creating amazing content
