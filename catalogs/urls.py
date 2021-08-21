from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ViewSet

from catalogs.views import CategoriesViewSet, Products, FeaturesViewSet, SearchViewset

app_name = 'catalogs'
router = DefaultRouter()
router.register(r'', CategoriesViewSet, basename='Categories')

urlpatterns = [
    path('<str:globalcategory>/<str:category>/', Products.as_view({'get': 'list', 'post': 'create'}), name='products'),
    path('<str:mainCategory>/<str:subCategory>/features/', FeaturesViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<str:mainCategory>/<str:subCategory>/search/', SearchViewset.as_view({'get': 'get'}))
]
urlpatterns += router.urls