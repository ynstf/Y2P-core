# YouTube Tutorial to Project Scaffold

An automated tool that watches programming tutorial videos and generates complete, runnable project scaffolds from them. Simply provide a YouTube URL, and the system will extract the transcript, analyze the code structure, and create a fully organized project directory with all files and folders.

## Features

- **Automatic Transcript Extraction**: Downloads video transcripts from YouTube tutorials
- **AI-Powered Code Analysis**: Uses Google Gemini AI to parse transcripts and identify project structure
- **Complete Project Generation**: Creates folders, files, and organizes code exactly as shown in tutorials
- **Ready-to-Run Output**: Generates a zipped project folder ready for immediate use
- **Smart Error Handling**: Handles common parsing issues and file format corrections

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

### Basic Usage

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

```bash
$ python main.py
put video URL : https://www.youtube.com/watch?v=nF_crEtmpBo
transcription ok: [transcript content]
manifest ok: {'folders': [...], 'files': {...}}
Project scaffolded and zipped as output\final_project.zip
```

### Advanced Usage

You can also use individual components:

```python
from download_transcript import get_youtube_transcript
from generate_manifest import generate_manifest_from_transcript
from scaffold_project import scaffold

# Get transcript
transcript = get_youtube_transcript("https://youtube.com/watch?v=VIDEO_ID")

# Generate manifest
manifest = generate_manifest_from_transcript()

# Create project
scaffold(manifest)
```

## Project Structure

```
youtube-tutorial-scaffold/
├── main.py                 # Main entry point
├── download_transcript.py  # YouTube transcript extraction
├── generate_manifest.py    # AI-powered manifest generation
├── scaffold_project.py     # Project file/folder creation
├── requirements.txt        # Python dependencies
├── .env-template          # Environment variables template
├── urls.txt              # Sample URLs for testing
└── output/               # Generated files directory
    ├── transcript.txt    # Raw video transcript
    ├── manifest.json     # Structured project manifest
    └── final_project/    # Generated project files
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Customization

You can modify the AI prompt in `generate_manifest.py` to:
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

### Debug Mode

Enable verbose output by modifying the print statements in each module to see detailed processing steps.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## Disclaimer

This tool is for educational purposes. Always respect:
- YouTube's Terms of Service
- Video creators' intellectual property rights
- API rate limits and usage policies

## Acknowledgments

- NoteGPT API for transcript extraction
- Google Gemini for AI-powered code analysis
- The programming tutorial community for creating amazing content
