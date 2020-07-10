from django.urls import re_path, include

from . import views

urlpatterns = [
    # overrides signup url in xauth
    re_path(r'^signup/', view=views.SignUpView.as_view(), name='signup', ),
    re_path(
        r'profile/(?P<username>\w+)/',
        view=views.ProfileView.as_view(),
        name='profile',
    ),
    re_path(r'^', include('xauth.urls', namespace='xauth')),
]
