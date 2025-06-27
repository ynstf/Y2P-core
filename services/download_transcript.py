import requests

# from urllib.parse import urlparse
import os
from .extract_youtube_id import extract_id


def get_youtube_transcript(youtube_url):
    # Extract video ID from YouTube URL
    # video_id = urlparse(youtube_url).path.split("/")[-1]
    video_id = extract_id(youtube_url)

    # API endpoint and parameters
    api_url = "https://notegpt.io/api/v2/video-transcript"
    params = {"platform": "youtube", "video_id": video_id}

    # Headers from the observed request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",
        "Accept": "*/*",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://notegpt.io/youtube-transcript-generator",
        "Connection": "keep-alive",
        "Cookie": (
            "sbox-guid=MTczMTUxNjAyM3w2MDV8OTQ3Njg3MTgw; "
            "_uab_collina=173151604203402789730031; "
            "_ga_PFX3BRW5RQ=GS1.1.1731606121.2.0.1731606121.60.0.825030076; "
            "_ga=GA1.2.147912956.1731516043; "
            "_trackUserId=G-1748946840000; "
            'g_state={"i_p":1752328996077,"i_l":4}; '
            "anonymous_user_id=677f88e861288a014e8350dd62e0f7da; "
            "is_first_visit=true; "
            "crisp-client%2Fsession%2F02aa9b53-fc37-4ca7-954d-7a99fb3393de=session_f7989467-2361-4bb6-9284-4197c29d7fe5; "
            "crisp-client%2Fsocket%2F02aa9b53-fc37-4ca7-954d-7a99fb3393de=0"
        ),
        "Host": "notegpt.io",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "Priority": "u=0",
    }

    # Make the API request
    response = requests.get(api_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # print(data)

        # Extract and format the transcript
        if data.get("code") == 100000:  # success code
            transcripts = data["data"]["transcripts"]
            lang = next(iter(transcripts))  # get first language

            # Combine all text segments
            full_transcript = ""
            for segment in transcripts[lang]["custom"]:
                full_transcript += segment["text"] + " "

            # FIXED: Use /tmp instead of output directory
            file_path_transcript = "/tmp/transcript.txt"

            # Ensure the /tmp directory exists (it should, but just in case)
            os.makedirs(os.path.dirname(file_path_transcript), exist_ok=True)

            with open(file_path_transcript, "w") as file:
                file.write(full_transcript.strip())

            return full_transcript.strip()
        else:
            return f"Error: {data.get('message')}"
    else:
        return f"Request failed with status: {response.status_code}"
