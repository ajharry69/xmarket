from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'payment'
urlpatterns = [
    re_path(r'^client-secret/', views.ClientSecretView.as_view(), name='stripe-client-secret', ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
