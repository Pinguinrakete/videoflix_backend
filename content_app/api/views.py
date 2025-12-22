from auth_app.api.permissions import CookieJWTAuthentication
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
    pass


class HLSVideoSegmentView(APIView):
    pass
