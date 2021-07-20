from django.urls import path
from rest_framework.routers import DefaultRouter

from catalogs.views import CategoriesViewSet, Products, FeaturesViewSet

app_name = 'catalogs'
router = DefaultRouter()
router.register(r'', CategoriesViewSet, basename='Sub_Categories')

urlpatterns = [
    # path('<str:mainCategory>/<str:subCategory>/', Products.as_view({'get': 'list', 'post': 'create'}), name='products'),
    # path('<str:mainCategory>/<str:subCategory>/features/', FeaturesViewSet.as_view({'get': 'list', 'post': 'create'})),
]
urlpatterns += router.urls