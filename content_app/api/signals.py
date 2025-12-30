import django_rq
import os
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from .jobs import video_processing_pipeline
from ..models import Video


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if not created or not instance.video:
        return

    queue = django_rq.get_queue("default")
    queue.enqueue(video_processing_pipeline, instance.id)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path)
