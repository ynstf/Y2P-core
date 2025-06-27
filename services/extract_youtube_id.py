from urllib.parse import urlparse, parse_qs


def extract_id(youtube_url: str) -> str:
    parsed = urlparse(youtube_url)
    # 1) If it’s a “youtu.be/…” short URL, the ID is in the path
    if parsed.netloc.endswith("youtu.be"):
        return parsed.path.lstrip("/")
    # 2) Otherwise, look for a “v” parameter in the query string
    qs = parse_qs(parsed.query)
    if "v" in qs and qs["v"]:
        return qs["v"][0]
    # 3) Fallback to last path segment (e.g. /embed/VIDEOID)
    return parsed.path.rstrip("/").split("/")[-1]


if __name__ == "__main__":
    url = input()
    id = extract_id(url)
    print("id : ", id)
