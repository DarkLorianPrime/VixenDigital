#  Copyright (c) 2023. Kasimov Alexander, Ulyanovsk. All right reserved.

from rest_framework.routers import DefaultRouter

from apps.products.views import ProductsViewSet, FeaturesViewSet

router = DefaultRouter()

router.register(f"features", FeaturesViewSet, basename="Feature")
router.register(f"", ProductsViewSet, basename="Product")

urlpatterns = router.urls
