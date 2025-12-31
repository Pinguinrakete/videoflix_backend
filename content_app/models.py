from django.db import models


CATEGORY_CHOICES = {
    ("drama", "Drama"),
    ("romance", "Romance"),
    ("action", "Action"),
    ("comedy", "Comedy"),
    ("horror", "Horror"),
    ("thriller", "Thriller"),
    ("sci_fi", "Science Fiction"),
    ("fantasy", "Fantasy"),
    ("documentary", "Documentary"),
    ("animation", "Animation"),
    ("adventure", "Adventure"),
    ("mystery", "Mystery"),
    ("crime", "Crime"),
    ("musical", "Musical"),
    ("music", "Music"),
    ("family", "Family"),
    ("biography", "Biography"),
    ("history", "History"),
    ("war", "War"),
    ("western", "Western"),
    ("sport", "Sport"),
}


class Video(models.Model):
    """
    Model for storing video metadata.

    This model represents a video including its title, description,
    thumbnail URL, category, and creation timestamp.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=False)
    video = models.FileField(upload_to="videos/")
    thumbnail_url = models.URLField(blank=True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    def __str__(self):
        return self.title
