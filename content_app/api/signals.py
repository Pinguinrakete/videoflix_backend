import django_rq
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from .jobs import video_cleanup_job
from .jobs import video_processing_pipeline
from ..models import Video


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if not created or not instance.video:
        return

    queue = django_rq.get_queue("default")
    queue.enqueue(video_processing_pipeline, instance.id)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    queue = django_rq.get_queue("default")

    queue.enqueue(
        video_cleanup_job,
        instance.id,
        instance.video.path if instance.video else None,
    )
