from pathlib import Path
from django.conf import settings
from ..models import Video
from .tasks import convert_to_hls
from .tasks import generate_thumbnail
from urllib.parse import urljoin


def video_processing_pipeline(video_id):
    video = Video.objects.get(id=video_id)
    source = video.video.path

    base_dir = Path(settings.MEDIA_ROOT) / "hls" / str(video.id)
    base_dir.mkdir(parents=True, exist_ok=True)

    for res in ["480p", "720p", "1080p"]:
        convert_to_hls(source, base_dir, res)

    create_master_playlist(base_dir)

    thumb_path = Path(
        settings.MEDIA_ROOT
        ) / "thumbnail" / f"image{video.id}.jpg"
    thumb_path.parent.mkdir(parents=True, exist_ok=True)

    generate_thumbnail(source, thumb_path)

    video.thumbnail_url = urljoin(
        settings.SITE_URL,
        f"{settings.MEDIA_URL}thumbnail/{thumb_path.name}"
    )
    video.save(update_fields=["thumbnail_url"])


def create_master_playlist(base_dir):
    master_dir = base_dir / "master"
    master_dir.mkdir(exist_ok=True)
    content = """#EXTM3U
#EXT-X-VERSION:3

#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=854x480
480p/index.m3u8

#EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=1280x720
720p/index.m3u8

#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1920x1080
1080p/index.m3u8
"""
    (master_dir / "index.m3u8").write_text(content)
