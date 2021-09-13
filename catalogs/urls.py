from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ViewSet

from catalogs.views import CategoryViewSet, Products, FeaturesViewSet, SearchViewset

app_name = 'catalogs'
router = DefaultRouter()
router.register(r'', CategoryViewSet, basename='Categories')

urlpatterns = [
    path('<str:catalog>/<str:category>/', Products.as_view({'get': 'list', 'post': 'create'}), name='products'),
    path('<str:catalog>/<str:category>/features/', FeaturesViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<str:catalog>/<str:category>/search/', SearchViewset.as_view({'get': 'get'}))
]
urlpatterns += router.urls