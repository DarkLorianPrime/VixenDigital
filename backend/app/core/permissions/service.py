from apps.organizations.models import Organization


class Service:
    def is_organization_exists(self, **kwargs) -> bool:
        return Organization.objects.filter(**kwargs).exists()

    def is_valid_user_admin_password(self, user, admin_password):
        return user.admin_code == int(admin_password)
