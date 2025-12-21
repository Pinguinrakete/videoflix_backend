from django.db import models

# from auth_app.models import Account


class Video(models.Model):
    """
    Model for storing video metadata.

    This model represents a video including its title, description,
    thumbnail URL, category, and creation timestamp.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=False)
    thumbnail_url = models.TextField(blank=True, default="")
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.title
