from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authorization.views import RegistrationViewSet, TokenViewSet

urlpatterns = [
    path('token/', TokenViewSet.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', RegistrationViewSet.as_view({'post': 'create'}), name="create_account")
]
