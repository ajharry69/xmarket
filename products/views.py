from rest_framework import permissions

from products.models import Product
from products.serializers import ProductSerializer
from xmarket.utils import views


class ProductViewMixin(object):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    lookup_fields = ['shop_id', 'pk']

    def get_queryset(self):
        return Product.objects.filter(shop_id=self.kwargs.get('shop_id'))


class ProductListView(ProductViewMixin, views.MultipleLookupListCreateView):
    def perform_create(self, serializer):
        serializer.save(shop_id=self.kwargs.get("shop_id"))


class ProductDetailView(ProductViewMixin, views.MultipleLookupRetrieveUpdateDestroyView):
    def perform_update(self, serializer):
        serializer.save(shop_id=self.kwargs.get("shop_id"))
