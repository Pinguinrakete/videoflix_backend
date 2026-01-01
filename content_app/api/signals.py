import django_rq
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from .jobs import video_cleanup_job
from .jobs import video_processing_pipeline
from ..models import Video


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Post-save signal handler for Video instances.

    Automatically enqueues the video processing pipeline when a new
    video is created and a video file is present.
    """

    if not created or not instance.video:
        return

    queue = django_rq.get_queue("default")
    queue.enqueue(video_processing_pipeline, instance.id)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    """
    Post-delete signal handler for Video instances.

    Automatically enqueues a cleanup job to remove all files
    associated with the deleted video, including the source file
    and generated streaming assets.
    """

    queue = django_rq.get_queue("default")

    queue.enqueue(
        video_cleanup_job,
        instance.id,
        instance.video.path if instance.video else None,
    )
