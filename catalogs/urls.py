from django.urls import path

from catalogs.views import Get_Codes, Sub_Category, Products, First_Page

app_name = 'catalogs'
urlpatterns = [
    # path('', Start_Page.as_view(), name='Start_Page'),
    path('', First_Page.as_view({'get': 'list', 'post': 'create'}), name='Start_Page'),
    path('codes', Get_Codes.as_view({'get': 'list', 'post': 'list'}), name='all_codes'),
    path('<str:mainCategory>/', Sub_Category.as_view({'get': 'list', 'post': 'create'}), name='Sub_Categories'),
    path('<str:mainCategory>/<str:subCategory>/', Products.as_view({'get': 'list'}), name='products')
]