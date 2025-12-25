import subprocess
from pathlib import Path
from PIL import Image


def convert_480p(source):
    target = source + '_480p.mp4'
    cmd = (
        'ffmpeg -i "./{src}" -s hd480 -c:v libx264 '
        '-crf 23 -c:a aac -strict -2 "./{tgt}"'
    ).format(src=source, tgt=target)
    subprocess.run(cmd)


def convert_720p(source):
    target = source + '_720p.mp4'
    cmd = (
        'ffmpeg -i "./{src}" -s hd720 -c:v libx264 '
        '-crf 23 -c:a aac -strict -2 "./{tgt}"'
    ).format(src=source, tgt=target)
    subprocess.run(cmd)


def convert_1080p(source):
    target = source + '_1080p.mp4'
    cmd = (
        'ffmpeg -i "./{src}" -s hd1080 -c:v libx264 '
        '-crf 23 -c:a aac -strict -2 "./{tgt}"'
    ).format(src=source, tgt=target)
    subprocess.run(cmd)


def generate_thumbnail(video_path, thumbnail_path, size=(320, 180)):
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
