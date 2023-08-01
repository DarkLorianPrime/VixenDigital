#  Copyright (c) 2023. Kasimov Alexander, Ulyanovsk. All right reserved.

from django.db.models import Q, QuerySet
from rest_framework.exceptions import ValidationError

from apps.authorization.models import User
from apps.organizations.models import Organization


class OrganizationRepository:
    def __init__(self):
        self.model = Organization

    def is_organization_exists(self, organization_name: str):
        return self.model.objects.filter(name=organization_name).exists()

    def get_maintainer(self, user: User) -> User:
        return self.model.objects.filter(Q(maintainer=user) | Q(contributors=user)).first().maintainer

    def organization_logo_delete(self, instance: Organization) -> None:
        instance.logo.delete()

    def get_contributors(self, contributors_list: list) -> QuerySet:
        return User.objects.filter(id__in=contributors_list).all()

    def is_exist_organization(self, name: str) -> str:
        if self.is_organization_exists(name):
            raise ValidationError('already exists', code=409)

        return name

    def get_organization(self, *args, **kwargs) -> Organization:
        return self.model.objects.filter(*args, **kwargs).first()
