import json

from rest_framework import parsers
from xauth.views.profile import ProfileView as XauthProfileView
from xauth.views.signup import SignUpView as XauthSignUpView

from user.serializers.profile.request import ProfileRequestWithPhotoSerializer
from user.serializers.profile.response import ProfileResponseSerializer
from user.serializers.signup.request import SignUpRequestWithPhotoSerializer
from user.serializers.signup.response import SignUpResponseSerializer


class SignUpView(XauthSignUpView):
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser,)
    serializer_class = SignUpRequestWithPhotoSerializer
    serializer_class_response = SignUpResponseSerializer

    def get_request_data(self, request):
        rd = request.data  # request data
        # rd1: {"user":{ "user": {}, "password": "12345" },"photo": <File>}
        photo, user, password = rd.get('photo'), rd.get('user'), rd.get('password')
        # if rd1 user retrieval failed, fallback to { "user": {}, "password": "12345" }
        user = rd if user is None else user
        # if user data was received as string decode it to dict
        user = json.loads(user) if isinstance(user, (str, bytes)) else user
        password = password or user.get('password')
        user = user.get('user', user)
        user['password'] = password
        user['photo'] = photo
        return user


class ProfileView(XauthProfileView):
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser,)
    serializer_class = ProfileRequestWithPhotoSerializer
    serializer_class_response = ProfileResponseSerializer
