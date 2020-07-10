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


class ProfileView(XauthProfileView):
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser,)
    serializer_class = ProfileRequestWithPhotoSerializer
    serializer_class_response = ProfileResponseSerializer
