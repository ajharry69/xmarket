from django.urls import include, re_path
from rest_framework import routers

from products.views import ProductsViewSet
from shop.views import ShopsViewSet

router = routers.DefaultRouter()
router.register(r'shops', ShopsViewSet)
router.register(r'products', ProductsViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^accounts/', include('user.urls')),
]
