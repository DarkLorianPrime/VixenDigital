from django.urls import path, include

from apps.authorization.views import RegistrationViewSet, UsersViewSet, ForceUserViewSet, AccessTokenHandler, \
    RefreshTokenHandler

urlpatterns = [
    path("token/", include([
        path("", AccessTokenHandler.as_view(), name='token_obtain_pair'),
        path("refresh/", RefreshTokenHandler.as_view(), name='token_refresh'),
        path("create/", RegistrationViewSet.as_view({'post': 'create'}, name="token_create"))
    ]), name="account_credentials"),
    path("account/", include([
            path("", UsersViewSet.as_view({"get": "get_self"}), name="get_info_about_self"),
            path("admin/", include([
                path("login/", ForceUserViewSet.as_view({"post": "check_admin_access"}), name="admin_login")
            ]))
    ]), name="account_control"),
    path("users/", include([
        path("", UsersViewSet.as_view({"get": "list"}), name="get_all_users")
    ]))
]
