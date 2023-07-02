from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.app.catalogs.views import CategoryViewSet, Products, FeaturesViewSet, SearchViewset

app_name = 'catalogs'
router = DefaultRouter()
router.register(r'', CategoryViewSet, basename='Categories')

urlpatterns = [
    path('<str:core>/<str:category>/', Products.as_view({'get': 'list', 'post': 'create'}), name='products'),
    path('<str:core>/<str:category>/features/', FeaturesViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<str:core>/<str:category>/search/', SearchViewset.as_view({'get': 'get'}))
]

urlpatterns += router.urls