from django.urls import path
from .views import VideoView
from .views import HLSMasterPlaylistView
from .views import HLSVideoSegmentView


"""
    URL routes for video streaming and HLS delivery API endpoints.

    Includes endpoints for:
    - General video access and metadata retrieval
    - Serving HLS master playlists (.m3u8) for adaptive streaming
    - Serving individual HLS video segments for playback
"""

urlpatterns = [
    path(
        "video/",
        VideoView.as_view(),
        name="video"
        ),
    path(
        "video/<int:movie_id>/<str:resolution>/index.m3u8",
        HLSMasterPlaylistView.as_view(),
        name="hls_master_playlist"
        ),
    path(
        "video/<int:movie_id>/<str:resolution>/<str:segment>/",
        HLSVideoSegmentView.as_view(),
        name="hls_video_segment"
        ),
]
