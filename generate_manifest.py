import re
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# ─── Load env vars ─────────────────────────────────────────────────────────────
load_dotenv()


def generate_manifest_from_transcript(
    transcript_path: str = r"output\\transcript.txt",
    output_path: str = r"output\\manifest.json",
) -> dict:
    # Configure with explicit settings
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    # Read transcript
    with open(transcript_path, "r") as f:
        print("\n\n\nread text : ")
        print("------------------------------------------")
        transcript = f.read()
        print(transcript)

    # Use more explicit prompt similar to AI Studio
    prompt = f"""
        You are given the transcript of a tutorial video that walks through building
        a structured project (folders, Python files, text files, etc.) and shows all code snippets.
        Output **only** a single valid JSON object (no markdown, no prose) with exactly these keys:

        {{
        "folders": [ "relative/path/to/folder", ... ],
        "files": {{
            "relative/path/to/file.py": "full contents of that file",
            ...
        }}
        }}

        Transcript:
        \"\"\"
        {transcript}
        \"\"\"

        Now output the JSON manifest **and nothing else**:
        """

    # Set up model with specific parameters
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",  # Use full flash model
        generation_config={"temperature": 1, "max_output_tokens": 8192, "top_p": 0.95},
    )

    # Generate content
    response = model.generate_content(prompt)
    raw_text = response.text

    # Improved JSON extraction
    try:
        # Find first { and last } to capture JSON
        json_start = raw_text.find("{")
        json_end = raw_text.rfind("}") + 1
        manifest_text = raw_text[json_start:json_end]

        # Handle markdown code fences
        manifest_text = re.sub(
            r"^```(json)?|```$", "", manifest_text, flags=re.MULTILINE
        )
        manifest = json.loads(manifest_text.strip())
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Failed to parse JSON: {e}")
        print("Raw response was:")
        print(raw_text)
        raise

    # Normalize file extensions
    files = manifest.get("files", {})
    normalized_files = {}
    for path, content in files.items():
        # Fix common extension mistakes
        new_path = re.sub(r"\.pi$", ".py", path)
        new_path = re.sub(r"\.js$", ".js", new_path)  # Ensure proper case
        normalized_files[new_path] = content
    manifest["files"] = normalized_files

    # Save to file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"✅ Manifest saved to {output_path}")
    return manifest
