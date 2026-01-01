from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from pathlib import Path
from rest_framework.test import APITestCase, APIClient
from .api.tasks import delete_video_files
from .models import Video


class VideoModelTest(TestCase):
    def test_video_creation(self):
        dummy_video = SimpleUploadedFile("test.mp4", b"dummy content")
        video = Video.objects.create(
            title="Test Video",
            description="Description of test video",
            video=dummy_video,
            category="drama"
        )

        self.assertEqual(video.title, "Test Video")
        self.assertEqual(video.category, "drama")
        self.assertIsNotNone(video.created_at)
        self.assertEqual(str(video), "Test Video")


class VideoViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.dummy_video = SimpleUploadedFile("test.mp4", b"dummy content")
        self.video = Video.objects.create(
            title="Video Test",
            description="Test description",
            video=self.dummy_video,
            category="action"
        )

    def test_get_videos(self):
        url = reverse("video")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Video Test")

    def test_hls_master_playlist_404(self):
        url = reverse("hls_master_playlist", args=[999, "720p"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TasksTest(TestCase):
    def test_delete_video_files_no_errors(self):
        video_id = 123
        video_path = "/tmp/nonexistent.mp4"
        delete_video_files(video_id=video_id, video_path=video_path)
        self.assertTrue(True)
