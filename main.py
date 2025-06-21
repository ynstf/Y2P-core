from services.download_transcript import get_youtube_transcript as transcript
from services.generate_manifest import (
    generate_manifest_from_transcript as generate_manifest,
)
from services.scaffold_project import scaffold


def main():
    # raw video transcript
    youtube_url = str(input("put vedio URL : "))
    transcription = transcript(youtube_url)
    print("transcription ok:", transcription)

    # generate manifest from transcript
    manifest = generate_manifest()
    print("manifest ok:", manifest)

    # scaffold project
    scaffold(manifest=manifest)


if __name__ == "__main__":
    main()
