from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from shop.models import Shop
from shop.serializers import ShopSerializer


class ShopsViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
