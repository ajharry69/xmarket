from django.urls import include, re_path
from rest_framework import routers

from article.views import ArticleViewSet
from products.views import ProductDetailView, ProductListView
from receipt.views import ReceiptsViewSet
from shop.views import ShopsViewSet
from shopping_list.views import ShoppingListViewSet

router = routers.DefaultRouter()
router.register(r'shops', ShopsViewSet)
router.register(r'receipts', ReceiptsViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'shopping-lists', ShoppingListViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^accounts/', include('user.urls')),
    re_path(
        r'^shops/(?P<shop_id>[0-9]+)/products/$',
        view=ProductListView.as_view(),
        name='product-list',
    ),
    re_path(
        r'^shops/(?P<shop_id>[0-9]+)/products/(?P<pk>[0-9]+)/$',
        view=ProductDetailView.as_view(),
        name='product-detail',
    ),
    re_path(
        r'^articles/(?P<article_id>[0-9]+)/',
        include('article.urls'),
    )
]
