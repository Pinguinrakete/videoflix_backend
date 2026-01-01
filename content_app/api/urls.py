from django.urls import path
from .views import VideoView
from .views import HLSMasterPlaylistView
from .views import HLSVideoSegmentView


"""
    URL patterns for video streaming and management.

    - "video/" → VideoView: Handles video listing and metadata.
    - "video/<movie_id>/<resolution>/index.m3u8" → HLSMasterPlaylistView:
      Serves the HLS master playlist for a specific video and resolution.
    - "video/<movie_id>/<resolution>/<segment>/" → HLSVideoSegmentView:
      Serves individual HLS video segments for streaming.
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
