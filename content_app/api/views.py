from rest_framework.views import APIView
from auth_app.api.permissions import CookieJWTAuthentication


class VideoView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    pass


class HLSMasterPlaylistView(APIView):
    pass


class HLSVideoSegmentView(APIView):
    pass
