from pathlib import Path
from django.conf import settings
from ..models import Video
from .tasks import convert_to_hls
from .tasks import generate_thumbnail


def get_thumbnail_path(video_id):
    return Path(settings.MEDIA_ROOT) / "thumbnails" / f"video_{video_id}.jpg"


def video_processing_pipeline(video_id):
    video = Video.objects.get(id=video_id)
    source = video.video.path

    base_dir = Path(settings.MEDIA_ROOT) / "hls" / str(video.id)
    base_dir.mkdir(parents=True, exist_ok=True)

    for res in ["480p", "720p", "1080p"]:
        convert_to_hls(source, base_dir, res)

    thumb_path = Path(
        settings.MEDIA_ROOT
        ) / "thumbnails" / f"video_{video.id}.jpg"
    thumb_path.parent.mkdir(parents=True, exist_ok=True)

    generate_thumbnail(source, thumb_path)

    video.thumbnail_url = f"{settings.MEDIA_URL}thumbnails/{thumb_path.name}"
    video.save(update_fields=["thumbnail_url"])


def create_master_playlist(base_dir):
    content = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=854x480
480p/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=1280x720
720p/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1920x1080
1080p/index.m3u8
"""
    master = base_dir / "master.m3u8"
    master.write_text(content)
