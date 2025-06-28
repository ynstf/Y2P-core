import re
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import time
import random


# FIXED: Use /tmp instead of relative paths
file_path_transcript = "/tmp/transcript.txt"
file_path_manifest = "/tmp/manifest.json"

# ─── Load env vars ─────────────────────────────────────────────────────────────
load_dotenv()


class APIKeyManager:
    """Manages multiple API keys with rotation and fallback logic"""

    def __init__(self, api_keys_string: str):
        """Initialize with semicolon-separated API keys"""
        self.api_keys = [
            key.strip() for key in api_keys_string.split(";") if key.strip()
        ]
        self.current_key_index = 0
        self.failed_keys = set()

        if not self.api_keys:
            raise ValueError("No valid API keys found in the configuration")

        print(f"✅ Loaded {len(self.api_keys)} API keys")

    def get_next_key(self) -> str:
        """Get the next available API key"""
        available_keys = [
            key for i, key in enumerate(self.api_keys) if i not in self.failed_keys
        ]

        if not available_keys:
            raise Exception("All API keys have been exhausted")

        # Use round-robin selection from available keys
        key_index = self.current_key_index % len(available_keys)
        selected_key = available_keys[key_index]

        # Find the original index of this key
        original_index = self.api_keys.index(selected_key)

        self.current_key_index = (self.current_key_index + 1) % len(available_keys)

        return selected_key, original_index

    def mark_key_failed(self, key_index: int, error: str):
        """Mark an API key as failed"""
        self.failed_keys.add(key_index)
        print(f"❌ API key #{key_index + 1} failed: {error}")
        print(f"📊 Remaining keys: {len(self.api_keys) - len(self.failed_keys)}")

    def has_available_keys(self) -> bool:
        """Check if there are still available keys"""
        return len(self.failed_keys) < len(self.api_keys)


def generate_manifest_from_transcript(
    transcript_path: str = file_path_transcript,
    output_path: str = file_path_manifest,
    max_retries_per_key: int = 2,
    retry_delay: float = 1.0,
) -> dict:
    """
    Generate manifest from transcript using multiple API keys with fallback

    Args:
        transcript_path: Path to transcript file
        output_path: Path to save manifest JSON
        max_retries_per_key: Maximum retries per API key before marking as failed
        retry_delay: Delay between retries in seconds

    Returns:
        dict: Generated manifest

    Raises:
        Exception: If all API keys fail or no valid response is generated
    """

    # Get API keys from environment
    api_keys_string = os.getenv("GEMINI_API_KEY")
    if not api_keys_string:
        raise ValueError("GEMINI_API_KEY environment variable not found")

    # Initialize API key manager
    key_manager = APIKeyManager(api_keys_string)

    # Read transcript
    with open(transcript_path, "r") as f:
        print("\n\n\nread text : ")
        print("------------------------------------------")
        transcript = f.read()
        print(transcript)

    # Use more explicit prompt similar to AI Studio
    prompt = f"""
        You are given the transcript of a tutorial video that walks through building
        a structured project (folders, Python files, or java files, or any programming language, text files, etc.) and shows all code snippets.
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

    # Try each API key until one works
    last_error = None

    while key_manager.has_available_keys():
        try:
            # Get next available API key
            api_key, key_index = key_manager.get_next_key()
            print(f"🔑 Trying API key #{key_index + 1}...")

            # Configure Gemini with current API key
            genai.configure(api_key=api_key)

            # Set up model with specific parameters
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",  # Use full flash model
                generation_config={
                    "temperature": 1,
                    "max_output_tokens": 8192,
                    "top_p": 0.95,
                },
            )

            # Try the current key with retries
            for attempt in range(max_retries_per_key):
                try:
                    print(
                        f"🔄 Attempt {attempt + 1}/{max_retries_per_key} with key #{key_index + 1}"
                    )

                    # Generate content
                    response = model.generate_content(prompt)
                    raw_text = response.text

                    if not raw_text or raw_text.strip() == "":
                        raise Exception("Empty response from API")

                    # Improved JSON extraction
                    try:
                        # Find first { and last } to capture JSON
                        json_start = raw_text.find("{")
                        json_end = raw_text.rfind("}") + 1

                        if json_start == -1 or json_end <= json_start:
                            raise ValueError(
                                "No valid JSON structure found in response"
                            )

                        manifest_text = raw_text[json_start:json_end]

                        # Handle markdown code fences
                        manifest_text = re.sub(
                            r"^```(json)?|```$", "", manifest_text, flags=re.MULTILINE
                        )
                        manifest = json.loads(manifest_text.strip())

                        # Validate manifest structure
                        if not isinstance(manifest, dict):
                            raise ValueError("Manifest is not a valid dictionary")

                        if "folders" not in manifest or "files" not in manifest:
                            raise ValueError(
                                "Manifest missing required 'folders' or 'files' keys"
                            )

                        print(
                            f"✅ Successfully generated manifest with key #{key_index + 1}"
                        )

                        # Normalize file extensions
                        files = manifest.get("files", {})
                        normalized_files = {}
                        for path, content in files.items():
                            # Fix common extension mistakes
                            new_path = re.sub(r"\.pi$", ".py", path)
                            new_path = re.sub(
                                r"\.js$", ".js", new_path
                            )  # Ensure proper case
                            normalized_files[new_path] = content
                        manifest["files"] = normalized_files

                        # Save to file
                        with open(output_path, "w", encoding="utf-8") as f:
                            json.dump(manifest, f, indent=2, ensure_ascii=False)

                        print(f"✅ Manifest saved to {output_path}")
                        return manifest

                    except (ValueError, json.JSONDecodeError) as json_error:
                        error_msg = f"JSON parsing failed: {json_error}"
                        print(f"⚠️ {error_msg}")
                        print("Raw response preview:")
                        print(
                            raw_text[:500] + "..." if len(raw_text) > 500 else raw_text
                        )

                        if attempt == max_retries_per_key - 1:
                            raise Exception(error_msg)
                        else:
                            print(f"🔄 Retrying in {retry_delay} seconds...")
                            time.sleep(retry_delay)
                            continue

                except Exception as attempt_error:
                    error_msg = str(attempt_error)
                    print(f"⚠️ Attempt {attempt + 1} failed: {error_msg}")

                    if attempt == max_retries_per_key - 1:
                        # Mark this key as failed after all retries
                        key_manager.mark_key_failed(key_index, error_msg)
                        last_error = attempt_error
                        break
                    else:
                        print(f"🔄 Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)

                        # Add some randomization to avoid rate limiting
                        time.sleep(random.uniform(0.5, 1.5))

        except Exception as key_error:
            # This key failed completely
            error_msg = str(key_error)
            key_manager.mark_key_failed(key_index, error_msg)
            last_error = key_error
            continue

    # If we get here, all keys have failed
    error_message = f"All {len(key_manager.api_keys)} API keys have been exhausted. Last error: {last_error}"
    print(f"💥 {error_message}")
    raise Exception(error_message)
