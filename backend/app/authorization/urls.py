from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authorization.views import RegistrationViewSet, TokenViewSet, UsersViewSet

urlpatterns = [
    path('token/', TokenViewSet.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', RegistrationViewSet.as_view({'post': 'create'}), name="create_account"),
    path('users/', UsersViewSet.as_view({"get": "list"}), name="get_all_users"),
    path('users/me/', UsersViewSet.as_view({"get": "get"}), name="get_info_about_self"),
]
