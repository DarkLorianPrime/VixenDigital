from rest_framework.routers import DefaultRouter

from products.views import ProductsViewSet, FeaturesViewSet

router = DefaultRouter()
base_url = r"catalog/(?P<catalog>[0-9A-z-_]{1,128})\/(?P<category>[a-z0-9]+)"
router.register(f"{base_url}", ProductsViewSet, basename="Product")
router.register(f"{base_url}/features", FeaturesViewSet, basename="Feature")

urlpatterns = router.urls
