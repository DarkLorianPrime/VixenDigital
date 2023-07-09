from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from authorization.serializers import TokenSerializer
from authorization.views import RegistrationViewSet, UsersViewSet

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(serializer_class=TokenSerializer), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', RegistrationViewSet.as_view({'post': 'create'}), name="create_account"),
    path('users/', UsersViewSet.as_view({"get": "list"}), name="get_all_users"),
    path('users/me/', UsersViewSet.as_view({"get": "get"}), name="get_info_about_self"),
]
