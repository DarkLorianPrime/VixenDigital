from rest_framework.routers import SimpleRouter

from apps.catalogs.routers import CategoryRouter
from apps.catalogs.views import CatalogViewSet, CategoryViewSet, OrganizationViewSet

organization_router = SimpleRouter()
organization_router.register(r"brand", OrganizationViewSet, basename="Organization")

category_router = CategoryRouter()
category_router.register(r"(?P<catalog>[0-9A-z-_]{1,128})", CategoryViewSet, basename="Category")
category_router.register('', CatalogViewSet, basename='Catalog')

urlpatterns = [
    # path('<str:catalog>/<str:category>/search/', SearchViewset.as_view({'get': 'get'}))
]

urlpatterns += organization_router.urls
urlpatterns += category_router.urls
