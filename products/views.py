from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.serializers import ProductSerializer


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
