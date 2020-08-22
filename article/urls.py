from rest_framework import routers

from article import views

router = routers.DefaultRouter()
router.register(r'comments', views.CommentViewSet,)
urlpatterns = router.urls
