import subprocess
from pathlib import Path
from PIL import Image


def convert_to_hls(source, output_dir, resolution):
    """
    Converts a video to a specific resolution.
    :param source: Source file, e.g., "video.mp4"
    :param resolution: Target resolution
    as a string, e.g., "480p", "720p", "1080p"
    """

    resolutions = {
        "480p": "854x480",
        "720p": "1280x720",
        "1080p": "1920x1080",
    }

    if resolution not in resolutions:
        raise ValueError("Unsupported resolution")

    res_dir = output_dir / resolution
    res_dir.mkdir(parents=True, exist_ok=True)

    playlist = res_dir / "index.m3u8"

    cmd = [
        "ffmpeg",
        "-i", source,
        "-map", "0:v",
        "-map", "0:a?",
        "-vf", f"scale={resolutions[resolution]}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-f", "hls",
        "-hls_time", "4",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename",
        str(res_dir / "segment_%03d.ts"),
        str(playlist),
    ]

    subprocess.run(cmd, check=True)
    return playlist


def generate_thumbnail(video_path, thumbnail_path, size=(320, 320)):
    temp_frame = Path(thumbnail_path).with_suffix(".tmp.jpg")

    subprocess.run(
        [
            "ffmpeg",
            "-i", video_path,
            "-ss", "00:00:01",
            "-vframes", "1",
            str(temp_frame)
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    with Image.open(temp_frame) as img:
        img = img.convert("RGB")
        img.thumbnail(size)
        img.save(thumbnail_path, "JPEG", quality=85, optimize=True)

    temp_frame.unlink(missing_ok=True)
