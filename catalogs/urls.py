from django.urls import path

from catalogs.views import Start_Page, Codes, Sub_Category, Products

app_name = 'catalogs'
urlpatterns = [
    path('', Start_Page.as_view(), name='Start_Page'),
    path('codes', Codes.as_view(), name='all_codes'),
    path('<str:mainCategory>', Sub_Category.as_view(), name='Sub_Categories'),
    path('<str:mainCategory>/<str:subCategory>', Products.as_view(), name='products')
]