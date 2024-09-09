import json
import subprocess


def get_mediainfo_json(media_file_path: str) -> dict:
    mediainfo = {}

    try:
        result = subprocess.run(
            [
                "mediainfo",
                "-f",
                "--Output=JSON",
                media_file_path
            ],
            check=True,
            capture_output=True,
            text=True
        )
    except Exception as e:
        print(f"mediainfo error: {e}")
        return mediainfo

    if result.returncode == 0:
        mediainfo = json.loads(result.stdout)
    else:
        print(f"mediainfo error: {result.stderr}")
        mediainfo = {}

    return mediainfo