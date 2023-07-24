from django.urls import path, include

from apps.authorization.views import RegistrationViewSet, UsersViewSet, ForceUserViewSet, AccessTokenHandler, \
    RefreshTokenHandler

urlpatterns = [
    path("token/", include([
        path("", AccessTokenHandler.as_view(), name='token_obtain_pair'),
        path("refresh", RefreshTokenHandler.as_view(), name='token_refresh'),
    ]), name="account_credentials"),
    path('registration/', RegistrationViewSet.as_view({'post': 'create'}, name="create_account"), name="create_account"),
    path("users/", include([
        path("", UsersViewSet.as_view({"get": "list"}), name="get_all_users"),
        path("me/", include([
            path("", UsersViewSet.as_view({"get": "get_self"}), name="get_info_about_self"),
            path("admin/", ForceUserViewSet.as_view({"post": "check_admin_access"}))
        ]))
    ]))
]
