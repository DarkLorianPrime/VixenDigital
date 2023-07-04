from django.urls import path
from rest_framework.routers import DefaultRouter

from catalogs.views import CatalogViewSet, Products, FeaturesViewSet, SearchViewset, CategoryViewSet

router = DefaultRouter()
router.register(r"(?P<catalog>[0-9A-z-_]{1,128})", CategoryViewSet, basename="Category")
router.register(r'', CatalogViewSet, basename='Catalog')

urlpatterns = [
    path('<str:catalog>/<str:category>/', Products.as_view({'get': 'list', 'post': 'create'}), name='products'),
    path('<str:catalog>/<str:category>/features/', FeaturesViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<str:catalog>/<str:category>/search/', SearchViewset.as_view({'get': 'get'}))
]

urlpatterns += router.urls
