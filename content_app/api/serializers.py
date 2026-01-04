from rest_framework import serializers
from ..models import Video


class VideoSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.CharField(read_only=True)
    """
    Serializer for the Video model.

    Serializes basic video metadata including title, description,
    category, creation timestamp, and the associated thumbnail URL.
    """

    class Meta:
        model = Video
        fields = ["id",
                  "created_at",
                  "title",
                  "description",
                  "thumbnail_url",
                  "category"
                  ]
