from pathlib import Path
from django.core.files import File

from ..models import Video
from .tasks import generate_thumbnail


def create_video_thumbnail_job(video_id):
    video = Video.objects.get(id=video_id)

    video_path = video.video.path
    thumb_path = Path(video_path).with_suffix(".jpg")

    generate_thumbnail(video_path, thumb_path)

    with open(thumb_path, "rb") as f:
        video.thumbnail.save(thumb_path.name, File(f), save=True)
