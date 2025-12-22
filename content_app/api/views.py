import os
from auth_app.api.permissions import CookieJWTAuthentication
from django.conf import settings
from django.http import FileResponse, Http404
from models import Video
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import VideoSerializer


class VideoView(APIView):
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):

        videos = Video.objects.all().order_by("-created_at")
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HLSMasterPlaylistView(APIView):
    """
    Returns the HLS master playlist (index.m3u8)
    for a movie in a specific resolution.
    """

    authentication_classes = [CookieJWTAuthentication]

    def get(self, request, movie_id, resolution):
        if not Video.objects.filter(id=movie_id).exists():
            raise Http404("Video not found")

        manifest_path = os.path.join(
            settings.MEDIA_ROOT,
            "hls",
            str(movie_id),
            resolution,
            "index.m3u8",
        )

        if not os.path.exists(manifest_path):
            raise Http404("HLS manifest not found")

        return FileResponse(
            open(manifest_path, "rb"),
            content_type="application/vnd.apple.mpegurl",
        )


class HLSVideoSegmentView(APIView):
    pass
